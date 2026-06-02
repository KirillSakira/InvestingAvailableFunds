from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie
from app.scripts.funcs import fti
from .securitiesInfo import securitiesInfo


def _short_name(auth_user):
    name = f"{auth_user.last_name} {auth_user.first_name[0]}."

    if auth_user.patronymic:
        name += f" {auth_user.patronymic[0]}."

    return name


def enterpriseMainPage(request, uid=False):
    try:
        user_id = uid if uid else request.user.id
        name = ""

        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=user_id)
        )

        if uid:
            name = _short_name(auth_user)

        enterprise = auth_user.legacy_user.enterprise

        portfolio = Portfolio.objects.get(enterprise=enterprise)

        balance = portfolio.balance
        deposition = portfolio.deposition

        balance_change = balance - deposition
        balance_change_percentage = 0

        if deposition != 0:
            balance_change_percentage = float(balance_change) / (float(deposition) * 0.01)

        balance_info = {
            "balance": fti(balance),
            "var_balance": fti(balance_change),
            "balance_proc": fti(balance_change_percentage),
        }

        securities = (
            PortfolioToSecuritie.objects
            .filter(portfolio=portfolio)
            .select_related("securitie", "securitie__catalog")
        )

        balance_data = securitiesInfo(securities)

        return balance_info, balance_data, name

    except Exception:
        return "", "", "Error"