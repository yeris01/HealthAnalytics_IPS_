"""
Motor de Machine Learning para HealthAnalytics IPS
Modelos: Regresión Logística, Árbol de Decisión, Random Forest,
         Gradient Boosting, XGBoost (con SMOTE opcional)
Clustering: K-Means para segmentación de pacientes
Anomalías: Isolation Forest para detección de outliers
Interpretabilidad: SHAP values
"""
import os
import pickle
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.cluster import KMeans
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report,
                              roc_auc_score, silhouette_score)
from django.conf import settings

logger = logging.getLogger(__name__)

MODELO_PATH = os.path.join(settings.BASE_DIR, 'datasets', 'modelo_ml.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'datasets', 'scaler_ml.pkl')
CLUSTER_PATH = os.path.join(settings.BASE_DIR, 'datasets', 'cluster_ml.pkl')

FEATURES = ['edad', 'imc', 'glucosa', 'colesterol', 'presion_sistolica',
            'presion_diastolica', 'frecuencia_cardiaca', 'saturacion_oxigeno',
            'temperatura', 'fumador', 'antecedentes_familiares', 'consumo_alcohol']

TARGET = 'riesgo_enfermedad'


def obtener_datos_entrenamiento():
    from etl.models import Paciente
    qs = Paciente.objects.all().values(*FEATURES, TARGET)
    if not qs.exists():
        raise ValueError("No hay datos en la base de datos. Ejecute el ETL primero.")
    return pd.DataFrame(list(qs))


def preprocesar(df, usar_smote=False):
    df = df.copy()
    for col in ['fumador', 'antecedentes_familiares', 'consumo_alcohol']:
        df[col] = df[col].astype(int)
    X = df[FEATURES].fillna(df[FEATURES].median())
    y = df[TARGET]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    if usar_smote:
        try:
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state=42)
            X_scaled, y_encoded = smote.fit_resample(X_scaled, y_encoded)
            logger.info(f"SMOTE aplicado. Nuevas dimensiones: X={X_scaled.shape}, y={len(y_encoded)}")
        except Exception as e:
            logger.warning(f"SMOTE no disponible: {e}")
    return X_scaled, y_encoded, le, scaler


def entrenar_modelo(tipo_modelo='random_forest', usar_smote=False):
    df = obtener_datos_entrenamiento()
    X, y, le, scaler = preprocesar(df, usar_smote=usar_smote)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    modelos = {
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        'decision_tree': DecisionTreeClassifier(max_depth=10, random_state=42, class_weight='balanced'),
        'gradient_boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42),
        'xgboost': None,
    }
    if tipo_modelo == 'xgboost':
        try:
            from xgboost import XGBClassifier
            modelo = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4,
                                    random_state=42, eval_metric='mlogloss')
        except ImportError:
            logger.warning("XGBoost no instalado. Usando Random Forest.")
            modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    else:
        modelo = modelos.get(tipo_modelo, RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(modelo, X, y, cv=cv, scoring='accuracy')

    accuracy = round(accuracy_score(y_test, y_pred), 4)
    precision = round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    recall = round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    f1 = round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    cm = confusion_matrix(y_test, y_pred).tolist()
    clases = list(le.classes_)
    reporte = classification_report(y_test, y_pred, target_names=clases, output_dict=True, zero_division=0)

    rocauc = None
    try:
        if hasattr(modelo, 'predict_proba'):
            y_proba = modelo.predict_proba(X_test)
            rocauc = round(roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted'), 4)
    except Exception:
        pass

    importancias = {}
    if hasattr(modelo, 'feature_importances_'):
        importancias = dict(zip(FEATURES, [round(float(v), 4) for v in modelo.feature_importances_]))

    # SHAP explainability
    shap_values_list = None
    try:
        import shap
        if hasattr(modelo, 'feature_importances_'):
            explainer = shap.TreeExplainer(modelo)
            shap_values = explainer.shap_values(X_test[:100])
            if isinstance(shap_values, list):
                shap_values_list = [sv.tolist() for sv in shap_values]
            else:
                shap_values_list = shap_values.tolist()
    except Exception as e:
        logger.debug(f"SHAP no disponible: {e}")

    os.makedirs(os.path.dirname(MODELO_PATH), exist_ok=True)
    with open(MODELO_PATH, 'wb') as f:
        pickle.dump({'modelo': modelo, 'le': le, 'tipo': tipo_modelo}, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    resultado = {
        'tipo_modelo': tipo_modelo,
        'usar_smote': usar_smote,
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
        'shap_disponible': shap_values_list is not None,
    }
    logger.info(f"Modelo {tipo_modelo} (SMOTE={usar_smote}) entrenado. Accuracy: {accuracy}")
    return resultado


def segmentar_pacientes(n_clusters=4):
    from etl.models import Paciente
    qs = Paciente.objects.all().values(*FEATURES)
    if not qs.exists():
        raise ValueError("No hay datos en la base de datos.")
    df = pd.DataFrame(list(qs))
    for col in ['fumador', 'antecedentes_familiares', 'consumo_alcohol']:
        df[col] = df[col].astype(int)
    X = df[FEATURES].fillna(df[FEATURES].median())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, labels)
    pacientes = list(Paciente.objects.all())
    for p, cluster_id in zip(pacientes, labels):
        p.cluster = int(cluster_id)
        p.save(update_fields=['cluster'])
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    perfil_clusters = {}
    for i in range(n_clusters):
        mask = labels == i
        cluster_df = df.iloc[mask]
        perfil_clusters[int(i)] = {
            'total': int(mask.sum()),
            'edad_media': round(float(cluster_df['edad'].mean()), 1),
            'imc_medio': round(float(cluster_df['imc'].mean()), 1),
            'glucosa_media': round(float(cluster_df['glucosa'].mean()), 1),
        }
    os.makedirs(os.path.dirname(CLUSTER_PATH), exist_ok=True)
    with open(CLUSTER_PATH, 'wb') as f:
        pickle.dump({'kmeans': kmeans, 'scaler': scaler, 'n_clusters': n_clusters}, f)
    return {
        'n_clusters': n_clusters,
        'silhouette_score': round(float(sil_score), 4),
        'perfil_clusters': perfil_clusters,
        'total_pacientes': len(pacientes),
        'inercias': [round(float(kmeans.inertia_), 2)],
    }


def detectar_anomalias(contamination=0.05):
    from etl.models import Paciente
    qs = Paciente.objects.all().values(*FEATURES)
    if not qs.exists():
        raise ValueError("No hay datos en la base de datos.")
    df = pd.DataFrame(list(qs))
    for col in ['fumador', 'antecedentes_familiares', 'consumo_alcohol']:
        df[col] = df[col].astype(int)
    X = df[FEATURES].fillna(df[FEATURES].median())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    iso = IsolationForest(contamination=contamination, random_state=42)
    anomalias = iso.fit_predict(X_scaled)
    n_anomalias = int((anomalias == -1).sum())
    pacientes = list(Paciente.objects.all())
    for p, es_anomalia in zip(pacientes, anomalias):
        p.es_anomalia = bool(es_anomalia == -1)
        p.save(update_fields=['es_anomalia'])
    return {
        'total_pacientes': len(pacientes),
        'anomalias_detectadas': n_anomalias,
        'porcentaje_anomalias': round(float(n_anomalias / len(pacientes) * 100), 2),
        'contamination': contamination,
    }


def predecir_paciente(datos_paciente: dict):
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
    # SHAP explanation para este paciente
    explicacion = None
    try:
        import shap
        if hasattr(modelo, 'feature_importances_'):
            explainer = shap.TreeExplainer(modelo)
            shap_values = explainer.shap_values(X_scaled)
            if isinstance(shap_values, list):
                shap_individual = [float(shap_values[i][0][0]) for i in range(len(FEATURES))]
            else:
                shap_individual = [float(shap_values[0][i]) for i in range(len(FEATURES))]
            feat_imp = sorted(zip(FEATURES, shap_individual), key=lambda x: abs(x[1]), reverse=True)
            explicacion = [{'feature': f, 'impacto': round(v, 4)} for f, v in feat_imp[:5]]
    except Exception:
        pass
    return {
        'riesgo_predicho': riesgo_predicho,
        'probabilidades': probabilidades,
        'confianza': round(float(max(pred_proba)), 4),
        'explicacion_shap': explicacion,
    }


def predecir_todos_pacientes():
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
