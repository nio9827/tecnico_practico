from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


# ─────────────────────────────────────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────────────────────────────────────

class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "placeholder": "usuario@empresa.com",
            "class": "form-control",
        }),
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "••••••••",
            "class": "form-control",
        }),
    )
    remember_me = forms.BooleanField(required=False, label=_("Recordarme"))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email    = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Correo o contraseña incorrectos. Verifique sus datos.")
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(_("Esta cuenta está inactiva."))
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


# ─────────────────────────────────────────────────────────────────────────────
# Cambio de contraseña (usuario autenticado)
# ─────────────────────────────────────────────────────────────────────────────

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Extiende el formulario nativo de Django agregando clases CSS.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


# ─────────────────────────────────────────────────────────────────────────────
# Recuperación de contraseña via email (usuario NO autenticado)
# ─────────────────────────────────────────────────────────────────────────────

class CustomPasswordResetForm(PasswordResetForm):
    """
    Envía el email de recuperación usando el backend SMTP configurado.
    Django maneja internamente el envío; aquí solo añadimos estilos.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "usuario@empresa.com",
        })


class CustomSetPasswordForm(SetPasswordForm):
    """
    Formulario para establecer nueva contraseña desde el link del email.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


# ─────────────────────────────────────────────────────────────────────────────
# Registro (solo admin puede crear usuarios desde el panel)
# Se expone también como form para uso programático si se necesita.
# ─────────────────────────────────────────────────────────────────────────────

class UserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model  = CustomUser
        fields = ("email", "username", "first_name", "last_name", "role")
        widgets = {f: forms.TextInput(attrs={"class": "form-control"})
                   for f in ("username", "first_name", "last_name")}

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(_("Las contraseñas no coinciden."))
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user