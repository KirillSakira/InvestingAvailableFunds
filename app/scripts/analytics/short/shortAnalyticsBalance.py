from app.models import AuthUserExtra, Portfolio


def shortAnalyticsBalance(request, uid=False):
    try:
        user_id = uid if uid else request.user.id

        auth_user = AuthUserExtra.objects.select_related("legacy_user").get(pk=user_id)

        portfolio = Portfolio.objects.get(
            enterprise__legacy_user=auth_user.legacy_user
        )

        balance = float(portfolio.balance)
        deposition = float(portfolio.deposition)

        balance_percent = "0"

        if deposition:
            balance_percent = str(round(100 * balance / deposition - 100, 2))

        if balance_percent[0] != "-":
            balance_percent = "+" + balance_percent

        return balance, balance_percent

    except Exception:
        return "Error", ""