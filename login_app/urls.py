from django.urls import path
from . import views

app_name = "login_app"

urlpatterns = [
    # ── Autenticación ────────────────────────────────────────────────────────
    path("base/", views.base, name="base"),
    path("",          views.login_view,  name="login"),
    path("logout/",   views.logout_view, name="logout"),
    path("admin-panel/",    views.dashboard_admin,    name="dashboard_admin"),
    path("analista-panel/", views.dashboard_analista, name="dashboard_analista"),
    path("usuarios/crear/",               views.crear_usuario,         name="crear_usuario"),
    path("usuarios/<int:user_id>/toggle/", views.toggle_usuario_activo, name="toggle_usuario"),
    path("cuenta/cambiar-password/", views.cambiar_password, name="cambiar_password"),

]


'''    


    # ── Dashboards ───────────────────────────────────────────────────────────

    # ── Gestión de usuarios (solo Admin) ─────────────────────────────────────

    # ── Cambio de contraseña (usuario autenticado) ───────────────────────────

    # ── Recuperación de contraseña via email ─────────────────────────────────
    path(
        "password-reset/",
        views.PasswordResetCustomView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        views.PasswordResetDoneCustomView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmCustomView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        views.PasswordResetCompleteCustomView.as_view(),
        name="password_reset_complete",
    ),'''