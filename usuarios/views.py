from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PerfilUsuario
from .forms import RegistroForm
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegistroSerializer
from rest_framework.authtoken.models import Token
from django.db import transaction



def login_usuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('bienvenida')
            else:
                messages.error(request, 'Contraseña incorrecta')
        else:
            messages.error(request, 'Correo no registrado')

    return render(request, 'login.html')


@login_required(login_url='login')
def bienvenida(request):
    return render(request, 'mensaje.html', {'nombre': request.user.username})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        form.cleaned_data['first_name'] + form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=form.cleaned_data['password1']
                    )
                    PerfilUsuario.objects.create(
                        usuario=user,
                        telefono=form.cleaned_data['telefono'],
                        rol=form.cleaned_data['rol']
                    )
                    messages.success(request, 'Usuario registrado correctamente')
                    return redirect('login')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Formulario no válido')
    else:
        form = RegistroForm()
        

    return render(request, 'registro.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

class RegistroAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Correo no registrado'}, status=status.HTTP_400_BAD_REQUEST)

        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            token, _ = Token.objects.get_or_create(user=user_auth)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)


class BienvenidaAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'mensaje': f'Hola, {request.user.username}'})
