from django import forms
from .models import Usuario
from django.contrib.auth import authenticate

class RegistroClienteForm(forms.Form):
    
    nombre = forms.CharField(
        max_length=150,
        error_messages={"required": "Escribe tu nombre."},
    )
    correo = forms.EmailField(
        error_messages={
            "required": "Escribe tu correo.",
            "invalid": "El correo no es válido. Ejemplo: nombre@correo.com",
        },
    )
    telefono = forms.RegexField(
        regex=r"^[0-9]{7,10}$",
        error_messages={
            "required": "Escribe tu teléfono.",
            "invalid": "El teléfono debe tener solo números (de 7 a 10 dígitos).",
        },
    )
    password = forms.CharField(
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "Escribe una contraseña.",
            "max_length": "La contraseña puede tener máximo 8 caracteres.",
        },
    )
    confirmar = forms.CharField(
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "Confirma tu contraseña.",
            "max_length": "La contraseña puede tener máximo 8 caracteres.",
        },
    )

    
    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        if Usuario.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado. Usa otro o inicia sesión."
            )
        return correo

    
    def clean(self):
        datos = super().clean()
        password = datos.get("password")
        confirmar = datos.get("confirmar")
        if password and confirmar and password != confirmar:
            self.add_error("confirmar", "Las contraseñas no son iguales.")
        return datos

    
    def guardar(self):
        datos = self.cleaned_data
        return Usuario.objects.create_user(
            username=datos["correo"],
            email=datos["correo"],
            password=datos["password"],
            first_name=datos["nombre"],
            telefono=datos["telefono"],
            rol=Usuario.Rol.CLIENTE,
        )

        class LoginForm(forms.Form):
    
    correo = forms.EmailField(
        error_messages={
            "required": "Escribe tu correo.",
            "invalid": "El correo no es válido. Ejemplo: nombre@correo.com",
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={"required": "Escribe tu contraseña."},
    )

    
    def clean(self):
        datos = super().clean()
        correo = datos.get("correo")
        password = datos.get("password")

        if correo and password:
            usuario = None
            # Buscamos el usuario por su correo ignorando mayúsculas/minúsculas
            usuario_db = Usuario.objects.filter(email__iexact=correo).first()
            if usuario_db:
                
                usuario = authenticate(username=usuario_db.username, password=password)

            if usuario is None:
                raise forms.ValidationError("Correo o contraseña incorrectos.")
            
            
            self.usuario = usuario

        return datos