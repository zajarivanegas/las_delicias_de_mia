from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .decorators import rol_requerido
from .forms import CrearCocineroForm, LoginForm, RegistroClienteForm
from .models import Usuario


# Vista para registrar nuevos clientes
def registro(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.guardar()
            # Iniciamos sesión de una vez y mandamos al usuario al inicio
            login(request, usuario)
            return redirect("inicio")
    else:
        form = RegistroClienteForm()

    return render(request, "registro.html", {"form": form})


# Vista para iniciar sesión
def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.usuario)
            
            # Revisamos si hay una URL pendiente a donde quería entrar el usuario
            siguiente = request.GET.get("next")
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente, allowed_hosts={request.get_host()}
            ):
                return redirect(siguiente)
            
            return redirect("inicio")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# Vista para cerrar sesión de forma segura por POST
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


# Redirige a cada usuario a su sección correspondiente según su rol
@login_required
def inicio(request):
    destinos = {
        Usuario.Rol.CLIENTE: "menu",
        Usuario.Rol.COCINERO: "cocina",
        Usuario.Rol.DUENA: "panel_admin",
    }
    return redirect(destinos.get(request.user.rol, "menu"))


# Vista protegida exclusiva para cocineros
@rol_requerido(Usuario.Rol.COCINERO)
def cocina(request):
    return render(request, "pagina_rol.html", {"titulo": "Vista de cocina"})


# Vista protegida exclusiva para la dueña del negocio
@rol_requerido(Usuario.Rol.DUENA)
def panel_admin(request):
    return render(request, "pagina_rol.html", {"titulo": "Panel de administración"})