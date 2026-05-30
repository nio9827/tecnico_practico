from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import CustomUser


def role_required(*roles):
    """
    Decorador que combina login_required + verificación de rol.

    Uso:
        @role_required(CustomUser.Role.ADMIN)
        def mi_vista(request): ...

        @role_required(CustomUser.Role.ADMIN, CustomUser.Role.ANALISTA)
        def otra_vista(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# Atajos de uso común
admin_required    = role_required(CustomUser.Role.ADMIN)
analista_required = role_required(CustomUser.Role.ANALISTA)
any_role_required = role_required(CustomUser.Role.ADMIN, CustomUser.Role.ANALISTA)