from django.db import transaction

from app.models import AuthUserExtra, Portfolio
from app.scripts.funcs import returnJson


def unlinkingAnAccount(request):
    uid = request.POST.get("uid")

    try:
        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=uid)
        )
    except AuthUserExtra.DoesNotExist:
        return returnJson(status="error", message="Пользователь не найден")

    enterprise = auth_user.legacy_user.enterprise

    if enterprise is None:
        return returnJson(status="error", message="Клиент не найден")

    with transaction.atomic():
        Portfolio.objects.filter(enterprise=enterprise).update(employee=None)

    return returnJson(status="success", message="Аккаунт отвязан успешно")