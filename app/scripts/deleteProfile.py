from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import transaction

from app.models import (
    AuthUserExtra,
    BalanceHistory,
    Employee,
    Enterprise,
    LegacyUser,
    OperationHistory,
    Portfolio,
    PortfolioToSecuritie,
    Queue,
    Request,
)
from app.front_app.viewBack.getUserData import getUserData
from app.scripts.funcs import returnJson


def delete_profile(request):
    id_post = request.POST.get("id")
    user_id = id_post if id_post is not None else request.user.id

    userData = getUserData(request, user_id)

    try:
        auth_user = (
            AuthUserExtra.objects
            .select_related(
                "legacy_user",
                "legacy_user__enterprise",
                "legacy_user__employee",
            )
            .get(pk=user_id)
        )
    except AuthUserExtra.DoesNotExist:
        return returnJson(status="error", message="Пользователь не найден")

    legacy_user = auth_user.legacy_user

    if legacy_user is None:
        return returnJson(status="error", message="Профиль пользователя не найден")

    with transaction.atomic():
        if userData["role"] == "enterprise":
            enterprise = legacy_user.enterprise

            if enterprise is None:
                return returnJson(status="error", message="Клиент не найден")

            portfolio = Portfolio.objects.get(enterprise=enterprise)

            Queue.objects.filter(portfolio=portfolio).delete()
            PortfolioToSecuritie.objects.filter(portfolio=portfolio).delete()
            OperationHistory.objects.filter(portfolio=portfolio).delete()
            BalanceHistory.objects.filter(portfolio=portfolio).delete()
            Request.objects.filter(portfolio=portfolio).delete()

            portfolio.delete()
            User.objects.filter(pk=user_id).delete()
            LegacyUser.objects.filter(pk=legacy_user.pk).delete()
            Enterprise.objects.filter(pk=enterprise.pk).delete()

        else:
            employee = legacy_user.employee

            if employee is None:
                return returnJson(status="error", message="Сотрудник не найден")

            Portfolio.objects.filter(employee=employee).update(employee=None)

            User.objects.filter(pk=user_id).delete()
            LegacyUser.objects.filter(pk=legacy_user.pk).delete()
            Employee.objects.filter(pk=employee.pk).delete()

    if id_post is None:
        logout(request)

    return returnJson(status="success", message="Ваш аккаунт был удалён")