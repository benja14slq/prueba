from django import forms
from django.contrib.auth.models import User
from .models import Rol

class RegistroForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=100)
    last_name = forms.CharField(label='Apellido', max_length=100)
    email = forms.EmailField(label='Correo electrónico')
    telefono = forms.CharField(label='Número Teléfono', max_length=20)
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), label='Rol')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Las constraseñas no coinciden")
        return cleaned_data