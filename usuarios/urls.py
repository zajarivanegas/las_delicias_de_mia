from django.urls import path
from . import views

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("inicio/", views.inicio, name="inicio"),
    path("cocina/", views.cocina, name="cocina"),
    path("panel/", views.panel_admin, name="panel_admin"),
]