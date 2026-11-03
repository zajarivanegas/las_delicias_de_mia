from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def rol_requerido(*roles):
    def decorador(vista):
        @login_required
        def envoltura(request, *args, **kwargs):
            if request.user.rol not in roles:
                return render(request, "usuarios/acceso_denegado.html", status=403)
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador