from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationAdminForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Panel de administración Django personalizado para CustomUser.
    """
    add_form  = UserCreationAdminForm
    model     = CustomUser

    # Columnas en el listado
    list_display   = ("email", "username", "get_full_name", "role", "is_active", "date_joined")
    list_filter    = ("role", "is_active", "is_staff")
    search_fields  = ("email", "username", "first_name", "last_name")
    ordering       = ("email",)

    # Campos al EDITAR un usuario existente
    fieldsets = (
        (None,                  {"fields": ("email", "username", "password")}),
        (_("Información personal"), {"fields": ("first_name", "last_name")}),
        (_("Rol y permisos"),   {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Fechas"),           {"fields": ("last_login", "date_joined")}),
    )

    # Campos al CREAR un usuario nuevo desde el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )