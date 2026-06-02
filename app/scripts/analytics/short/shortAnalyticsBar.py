from django.utils import timezone

from app.models import AuthUserExtra, BalanceHistory, Portfolio


def shortAnalyticsBar(request, uid=False):
    try:
        user_id = uid if uid else request.user.id

        auth_user = AuthUserExtra.objects.select_related("legacy_user").get(pk=user_id)

        portfolio = Portfolio.objects.get(
            enterprise__legacy_user=auth_user.legacy_user
        )

        data = BalanceHistory.objects.filter(
            portfolio=portfolio,
            balance_date__year=timezone.now().year,
        ).values_list(
            "balance_date",
            "balance",
        )

        month = [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        ]

        count = [0] * 12

        for balance_date, balance in data:
            count[balance_date.month - 1] = round(float(balance), 2)

        return month, count, sum(count)

    except Exception:
        return "Error", "", ""