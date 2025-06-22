from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegistroSerializer
from rest_framework.authtoken.models import Token



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
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('registro')
        
        username = f"{first_name}_{last_name}".lower().replace(" ", "_")
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        user.save()
        messages.success(request, 'Usuario registrado correctamente')
        return redirect('login')
        

    return render(request, 'registro.html')

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
