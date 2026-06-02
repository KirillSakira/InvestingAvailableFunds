from django.db import transaction

from app.models import AuthUserExtra, Portfolio
from app.scripts.funcs import returnJson
from app.scripts.mainPages.manager.managerMainModule import getPortfolioData


def clientAdd(request):
    username = request.POST.get("email")
    django_user_id = request.POST.get("id") or request.user.id

    try:
        client_auth = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(username=username)
        )
    except AuthUserExtra.DoesNotExist:
        return returnJson(status="error", message="Такого пользователя не существует")

    client_legacy_user = client_auth.legacy_user

    if not client_legacy_user or not client_legacy_user.enterprise_id:
        return returnJson(status="error", message="Такого клиента не существует")

    try:
        employee_auth = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__employee")
            .get(pk=django_user_id)
        )
    except AuthUserExtra.DoesNotExist:
        return returnJson(status="error", message="Сотрудник не найден")

    employee_legacy_user = employee_auth.legacy_user

    if not employee_legacy_user or not employee_legacy_user.employee_id:
        return returnJson(status="error", message="Сотрудник не найден")

    with transaction.atomic():
        portfolio = (
            Portfolio.objects
            .select_for_update()
            .select_related("employee", "enterprise")
            .get(enterprise=client_legacy_user.enterprise)
        )

        if portfolio.employee_id is not None:
            if portfolio.employee_id == employee_legacy_user.employee_id:
                return returnJson(status="error", message="Клиент уже работает с вами")

            return returnJson(status="error", message="Клиент уже работает с другим менеджером")

        portfolio.employee = employee_legacy_user.employee
        portfolio.save(update_fields=["employee"])

    portfolio_data = getPortfolioData(portfolio)
    portfolio_data["status"] = "success"
    portfolio_data["message"] = "Клиент добавлен"

    return returnJson(data=portfolio_data)