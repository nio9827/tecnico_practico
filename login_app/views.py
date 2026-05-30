from django.contrib import messages
from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from .decorators import admin_required, any_role_required
from .forms import (
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    LoginForm,
    UserCreationAdminForm,
)
from .models import CustomUser


# ─────────────────────────────────────────────────────────────────────────────
# Autenticación
# ─────────────────────────────────────────────────────────────────────────────


def base(request):
    return render(request, "base.html")



@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de inicio de sesión con email + contraseña."""

    # Si ya está autenticado, redirigir a su dashboard
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    form = LoginForm(request=request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        # Manejar "Recordarme"
        if not form.cleaned_data.get("remember_me"):
            request.session.set_expiry(0)       # sesión expira al cerrar el navegador
        else:
            request.session.set_expiry(60 * 60 * 24 * 14)  # 14 días

        login(request, user)
        messages.success(request, _(f"Bienvenido/a, {user.get_full_name() or user.email}"))
        return _redirect_by_role(user)

    return render(request, "login.html", {"form": form})


def logout_view(request):
    """Cierre de sesión (acepta GET y POST)."""
    logout(request)
    messages.info(request, _("Sesión cerrada correctamente."))
    return redirect("login_app:login")


# ─────────────────────────────────────────────────────────────────────────────
# Dashboards por rol
# ─────────────────────────────────────────────────────────────────────────────

@admin_required
def dashboard_admin(request):
    """Panel exclusivo para Administradores."""
    users = CustomUser.objects.all().order_by("role", "email")
    return render(request, "dashboard_admin.html", {
        "users": users,
        "total_admins":    users.filter(role=CustomUser.Role.ADMIN).count(),
        "total_analistas": users.filter(role=CustomUser.Role.ANALISTA).count(),
    })


@any_role_required
def dashboard_analista(request):
    """Panel para Analistas (y también accesible por Admins)."""
    return render(request, "dashboard_analista.html")


# ─────────────────────────────────────────────────────────────────────────────
# Gestión de usuarios (solo Admin)
# ─────────────────────────────────────────────────────────────────────────────

@admin_required
@require_http_methods(["GET", "POST"])
def crear_usuario(request):
    """El Admin puede crear nuevos usuarios asignándoles un rol."""
    form = UserCreationAdminForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, _(f"Usuario {user.email} creado exitosamente."))
        return redirect("login_app:dashboard_admin")

    return render(request, "crear_usuario.html", {"form": form})


@admin_required
def toggle_usuario_activo(request, user_id):
    """Activa / desactiva un usuario (el Admin no puede desactivarse a sí mismo)."""
    user = CustomUser.objects.get(pk=user_id)

    if user == request.user:
        messages.error(request, _("No puedes desactivarte a ti mismo."))
    else:
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])
        estado = _("activado") if user.is_active else _("desactivado")
        messages.success(request, _(f"Usuario {user.email} {estado}."))

    return redirect("login_app:dashboard_admin")


# ─────────────────────────────────────────────────────────────────────────────
# Cambio de contraseña (usuario autenticado)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(["GET", "POST"])
def cambiar_password(request):
    """
    Permite al usuario cambiar su contraseña.
    Usa update_session_auth_hash para no cerrar la sesión al cambiarla.
    """
    form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)   # mantiene la sesión activa
        messages.success(request, _("Contraseña actualizada correctamente."))
        return _redirect_by_role(request.user)

    return render(request, "cambiar_password.html", {"form": form})


# ─────────────────────────────────────────────────────────────────────────────
# Recuperación de contraseña via email (flujo nativo de Django + SMTP Gmail)
# ─────────────────────────────────────────────────────────────────────────────

class PasswordResetCustomView(PasswordResetView):
    """
    Paso 1: el usuario ingresa su email.
    Django genera un token seguro y envía el email de recuperación
    usando el backend SMTP configurado en settings.py (Gmail).
    """
    template_name      = "password_reset_form.html"
    email_template_name = "emails/password_reset_email.html"
    subject_template_name = "emails/password_reset_subject.txt"
    form_class         = CustomPasswordResetForm
    success_url        = reverse_lazy("login_app:password_reset_done")
    # Enviar solo a usuarios activos
    extra_email_context = {"site_name": "Sistema de Gestión"}


class PasswordResetDoneCustomView(PasswordResetDoneView):
    """Paso 2: confirmación de que el email fue enviado."""
    template_name = "password_reset_done.html"


class PasswordResetConfirmCustomView(PasswordResetConfirmView):
    """Paso 3: el usuario ingresa su nueva contraseña desde el link del email."""
    template_name = "password_reset_confirm.html"
    form_class    = CustomSetPasswordForm
    success_url   = reverse_lazy("login_app:password_reset_complete")


class PasswordResetCompleteCustomView(PasswordResetCompleteView):
    """Paso 4: contraseña reestablecida con éxito."""
    template_name = "password_reset_complete.html"


# ─────────────────────────────────────────────────────────────────────────────
# Helper interno
# ─────────────────────────────────────────────────────────────────────────────

def _redirect_by_role(user):
    """Redirige al dashboard correspondiente según el rol del usuario."""
    if user.role == CustomUser.Role.ADMIN:
        return redirect("login_app:dashboard_admin")
    return redirect("login_app:dashboard_analista")