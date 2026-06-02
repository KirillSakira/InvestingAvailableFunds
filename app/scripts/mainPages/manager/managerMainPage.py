from app.models import AuthUserExtra, Portfolio
from .managerMainModule import getPortfolioData


def managerMainPage(request, uid=False):
    try:
        user_id = uid if uid else request.user.id

        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__employee")
            .get(pk=user_id)
        )

        employee = auth_user.legacy_user.employee

        portfolios = (
            Portfolio.objects
            .filter(employee=employee)
            .select_related("enterprise")
        )

        return [getPortfolioData(portfolio) for portfolio in portfolios]

    except Exception:
        return "Error"