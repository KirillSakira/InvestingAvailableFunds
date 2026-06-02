from app.models import AuthUserExtra
from app.scripts.funcs import fti


def getPortfolioData(portfolio):
    uid, initials = getInitials(portfolio.enterprise_id)

    balance = portfolio.balance
    deposition = portfolio.deposition

    balance_change = 0

    if deposition:
        balance_change = fti((float(balance) / float(deposition) - 1) * 100)

    return {
        "id": uid,
        "name": initials,
        "balance": fti(balance),
        "balance_proc": fti(balance_change),
    }


def getInitials(id_enterprise):
    auth_user = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .get(legacy_user__enterprise_id=id_enterprise)
    )

    initials = f"{auth_user.last_name} {auth_user.first_name[0]}."

    if auth_user.patronymic:
        initials += f" {auth_user.patronymic[0]}."

    return auth_user.id, initials