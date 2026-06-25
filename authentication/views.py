from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from .serializers import CustomTokenObtainPairSerializer, RegistroUsuarioSerializer, UsuarioSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@permission_classes([AllowAny])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        error = 'Usuario o contraseña incorrectos.'
    return render(request, 'authentication/login.html', {'error': error})

@login_required
def logout_view(request):
    logout(request)
    return redirect('authentication:login')

@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario(request):
    serializer = RegistroUsuarioSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    usuario = serializer.save()
    return Response(UsuarioSerializer(usuario).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    if request.method == 'GET':
        return Response(UsuarioSerializer(request.user).data)
    serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def listar_usuarios(request):
    return Response(UsuarioSerializer(Usuario.objects.all().order_by('username'), many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    return Response({'detail': 'Sesión API finalizada en el cliente. Elimine el token local.'})
