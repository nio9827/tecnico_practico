from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Usuario personalizado con soporte para roles.
    Extiende AbstractUser para mantener toda la funcionalidad
    nativa de autenticación de Django.
    """

    class Role(models.TextChoices):
        ADMIN    = "admin",    "Administrador"
        ANALISTA = "analista", "Analista"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ANALISTA,
        verbose_name="Rol",
    )
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")

    # El login se hará con email en lugar de username
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name        = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering            = ["email"]

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}> [{self.get_role_display()}]"

    # ── helpers de rol ──────────────────────────────────────────
    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_analista_role(self):
        return self.role == self.Role.ANALISTA