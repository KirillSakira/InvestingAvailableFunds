from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie, Queue, Security
from app.scripts.funcs import fti, numFormat
from app.scripts.trading.getPromotionsNew import get_graph_info


def getSecuritieInfo(request, userId, ticker):
    type = {
        1: {
            "eng": "stocks",
            "rus": "акций",
            "href_rus": "акции",
        },
        2: {
            "eng": "bonds",
            "rus": "облигаций",
            "href_rus": "облигации",
        },
        3: {
            "eng": "funds",
            "rus": "фондов",
            "href_rus": "фонды",
        },
        4: {
            "eng": "curr_metals",
            "rus": "ценных металлов",
            "href_rus": "ценные металлы",
        },
    }

    auth_user = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .get(pk=userId)
    )

    portfolio = Portfolio.objects.get(
        enterprise=auth_user.legacy_user.enterprise
    )

    security = Security.objects.get(ticker=ticker)

    first_queue_item = (
        Queue.objects
        .filter(
            portfolio=portfolio,
            securitie=security,
        )
        .order_by("queue_date")
        .first()
    )

    if first_queue_item:
        oldPrice = first_queue_item.quotation
        newPrice = security.quotation
        proc = 100 - (float(oldPrice) / float(newPrice)) * 100 if newPrice else 0
    else:
        proc = 0

    security_link = (
        PortfolioToSecuritie.objects
        .filter(
            portfolio=portfolio,
            securitie=security,
        )
        .first()
    )

    rub_link = (
        PortfolioToSecuritie.objects
        .filter(
            portfolio=portfolio,
            securitie_id=36,
        )
        .first()
    )

    totalQuantity = security_link.total_quantity if security_link else 0
    balance = rub_link.total_quantity if rub_link else 0

    graphLine = get_graph_info(ticker, type[security.catalog_id]["href_rus"])

    data = {
        "security_name": security.sec_name,
        "security_price": fti(float(graphLine["1 day"][-1]["price"]) if len(graphLine["1 day"]) else 0),
        "security_img": security.icon,
        "graph_line": graphLine,
        "proc": fti(proc),
        "total_sum": fti(fti(security.quotation) * fti(totalQuantity)),
        "total_quantity1": numFormat(fti(totalQuantity)),
        "balance": numFormat(fti(balance)),
        "type": type[security.catalog_id],
    }

    return data