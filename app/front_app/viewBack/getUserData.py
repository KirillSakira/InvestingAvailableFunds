from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie
from app.scripts.funcs import fti


def getUserData(request, uid=False, initial=False):
    user_id = uid if uid else request.user.id

    auth_user = (
        AuthUserExtra.objects
        .select_related(
            "legacy_user",
            "legacy_user__employee",
            "legacy_user__employee__post",
            "legacy_user__enterprise",
        )
        .get(pk=user_id)
    )

    if initial:
        name = f"{auth_user.last_name} {auth_user.first_name[0]}."
        if auth_user.patronymic:
            name += f" {auth_user.patronymic[0]}."
    else:
        name = f"{auth_user.last_name} {auth_user.first_name}"
        if auth_user.patronymic:
            name += f" {auth_user.patronymic}"

    legacy_user = auth_user.legacy_user

    if legacy_user.employee_id is None:
        portfolio = Portfolio.objects.get(enterprise=legacy_user.enterprise)

        rub_link = PortfolioToSecuritie.objects.get(
            portfolio=portfolio,
            securitie_id=36,
        )

        return {
            "id": user_id,
            "name": name,
            "role": "enterprise",
            "balance": f"{fti(rub_link.total_quantity):,.0f}".replace(",", " "),
        }

    post_name = legacy_user.employee.post.post_name
    role = "Admin" if post_name == "Администратор" else "Manager"

    return {
        "id": user_id,
        "name": name,
        "role": role,
    }