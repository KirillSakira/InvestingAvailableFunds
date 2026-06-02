from app.models import AuthUserExtra, Portfolio, Request
from app.scripts.funcs import fti


def trading_history(uid):
    auth_user = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .get(pk=uid)
    )

    portfolio = Portfolio.objects.get(
        enterprise=auth_user.legacy_user.enterprise
    )

    requests = (
        Request.objects
        .filter(
            portfolio=portfolio,
            req_status=True,
        )
        .select_related("securitie")
        .order_by("-req_date")
    )

    request_types = ["Продажа", "Покупка"]

    data = []

    for request in requests:
        security = request.securitie

        data.append(
            {
                "name": security.sec_name,
                "short_name": security.ticker,
                "img": security.icon,
                "type": request_types[int(request.req_type)],
                "price": fti(request.total_price),
                "count": fti(request.quantity),
                "datetime": request.req_date,
                "date": request.req_date.strftime("%d.%m.%Y"),
                "time": request.req_date.strftime("%H:%M"),
            }
        )

    return data