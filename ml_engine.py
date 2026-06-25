"""
Motor de Machine Learning para HealthAnalytics IPS
Modelos: Regresión Logística, Árbol de Decisión, Random Forest, Gradient Boosting
"""
import os
import pickle
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report,
                              roc_auc_score)
from sklearn.model_selection import StratifiedKFold
from django.conf import settings

logger = logging.getLogger(__name__)

MODELO_PATH = os.path.join(settings.BASE_DIR, 'datasets', 'modelo_ml.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'datasets', 'scaler_ml.pkl')

FEATURES = ['edad', 'imc', 'glucosa', 'colesterol', 'presion_sistolica',
            'presion_diastolica', 'frecuencia_cardiaca', 'saturacion_oxigeno',
            'temperatura', 'fumador', 'antecedentes_familiares', 'consumo_alcohol']

TARGET = 'riesgo_enfermedad'


def obtener_datos_entrenamiento():
    """Obtiene datos de la BD y los prepara para ML."""
    from etl.models import Paciente
    qs = Paciente.objects.all().values(*FEATURES, TARGET)
    if not qs.exists():
        raise ValueError("No hay datos en la base de datos. Ejecute el ETL primero.")
    df = pd.DataFrame(list(qs))
    return df


def preprocesar(df):
    """Preprocesa el DataFrame para entrenamiento."""
    df = df.copy()
    for col in ['fumador', 'antecedentes_familiares', 'consumo_alcohol']:
        df[col] = df[col].astype(int)

    X = df[FEATURES].fillna(df[FEATURES].median())
    y = df[TARGET]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y_encoded, le, scaler


def entrenar_modelo(tipo_modelo='random_forest'):
    """Entrena el modelo seleccionado y guarda artefactos."""
    df = obtener_datos_entrenamiento()
    X, y, le, scaler = preprocesar(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if tipo_modelo == 'logistic_regression':
        modelo = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    elif tipo_modelo == 'decision_tree':
        modelo = DecisionTreeClassifier(max_depth=10, random_state=42, class_weight='balanced')
    elif tipo_modelo == 'gradient_boosting':
        modelo = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    else:  # random_forest (default)
        modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    # Validación cruzada (5-fold)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(modelo, X, y, cv=cv, scoring='accuracy')

    # Métricas
    accuracy = round(accuracy_score(y_test, y_pred), 4)
    precision = round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    recall = round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    f1 = round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    cm = confusion_matrix(y_test, y_pred).tolist()
    clases = list(le.classes_)

    # Reporte detallado por clase
    reporte = classification_report(y_test, y_pred, target_names=clases, output_dict=True, zero_division=0)

    # ROC AUC (uno vs resto para multiclase)
    try:
        if hasattr(modelo, 'predict_proba'):
            y_proba = modelo.predict_proba(X_test)
            rocauc = round(roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted'), 4)
        else:
            rocauc = None
    except Exception:
        rocauc = None

    # Importancia de características (si aplica)
    importancias = {}
    if hasattr(modelo, 'feature_importances_'):
        importancias = dict(zip(FEATURES, [round(float(v), 4) for v in modelo.feature_importances_]))

    # Guardar modelo y scaler
    os.makedirs(os.path.dirname(MODELO_PATH), exist_ok=True)
    with open(MODELO_PATH, 'wb') as f:
        pickle.dump({'modelo': modelo, 'le': le, 'tipo': tipo_modelo}, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    resultado = {
        'tipo_modelo': tipo_modelo,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'clases': clases,
        'importancia_features': importancias,
        'total_entrenamiento': len(X_train),
        'total_prueba': len(X_test),
        'cv_accuracy_mean': round(float(cv_scores.mean()), 4),
        'cv_accuracy_std': round(float(cv_scores.std()), 4),
        'roc_auc': rocauc,
        'reporte_por_clase': {
            cls: {m: round(float(reporte[cls][m]), 4) for m in ['precision', 'recall', 'f1-score']}
            for cls in clases if cls in reporte
        },
    }
    logger.info(f"Modelo {tipo_modelo} entrenado. Accuracy: {accuracy}")
    return resultado


def predecir_paciente(datos_paciente: dict):
    """Predice el riesgo de un paciente individual."""
    if not os.path.exists(MODELO_PATH):
        raise FileNotFoundError("Modelo no entrenado. Ejecute el entrenamiento primero.")

    with open(MODELO_PATH, 'rb') as f:
        artefacto = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    modelo = artefacto['modelo']
    le = artefacto['le']

    valores = []
    for feat in FEATURES:
        val = datos_paciente.get(feat, 0)
        if isinstance(val, bool):
            val = int(val)
        valores.append(float(val) if val is not None else 0.0)

    X = np.array(valores).reshape(1, -1)
    X_scaled = scaler.transform(X)

    pred_encoded = modelo.predict(X_scaled)[0]
    pred_proba = modelo.predict_proba(X_scaled)[0]

    riesgo_predicho = le.inverse_transform([pred_encoded])[0]
    clases = list(le.classes_)
    probabilidades = {cls: round(float(prob), 4) for cls, prob in zip(clases, pred_proba)}

    return {
        'riesgo_predicho': riesgo_predicho,
        'probabilidades': probabilidades,
        'confianza': round(float(max(pred_proba)), 4),
    }


def predecir_todos_pacientes():
    """Aplica predicciones a todos los pacientes en BD y actualiza su riesgo."""
    from etl.models import Paciente

    if not os.path.exists(MODELO_PATH):
        raise FileNotFoundError("Modelo no entrenado.")

    with open(MODELO_PATH, 'rb') as f:
        artefacto = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    modelo = artefacto['modelo']
    le = artefacto['le']

    pacientes = Paciente.objects.all()
    actualizados = 0

    for p in pacientes:
        datos = {feat: getattr(p, feat, 0) for feat in FEATURES}
        valores = []
        for feat in FEATURES:
            val = datos.get(feat, 0)
            if isinstance(val, bool):
                val = int(val)
            valores.append(float(val) if val is not None else 0.0)

        X = np.array(valores).reshape(1, -1)
        X_scaled = scaler.transform(X)
        pred = modelo.predict(X_scaled)[0]
        riesgo = le.inverse_transform([pred])[0]
        p.riesgo_enfermedad = riesgo
        p.evaluar_criticidad()
        p.save(update_fields=['riesgo_enfermedad', 'es_critico'])
        actualizados += 1

    return actualizados
