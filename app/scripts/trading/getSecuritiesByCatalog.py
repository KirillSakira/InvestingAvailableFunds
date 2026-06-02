from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie, Security
from app.scripts.funcs import fti
from app.scripts.trading.getPromotionsNew import get_last_prices_by_tickers


def getSecuritiesByCatalog(request, userId):
    auth_user = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .get(pk=userId)
    )

    portfolio = Portfolio.objects.get(
        enterprise=auth_user.legacy_user.enterprise
    )

    portfolio_quantities = {
        item.securitie_id: item.total_quantity
        for item in PortfolioToSecuritie.objects.filter(portfolio=portfolio)
    }

    data = {
        "stocks_data": [],
        "bonds_data": [],
        "funds_data": [],
        "curr_metals_data": [],
    }

    template = [
        "",
        "stocks_data",
        "bonds_data",
        "funds_data",
        "curr_metals_data",
    ]

    securities = (
        Security.objects
        .select_related("catalog")
        .all()
        .order_by("id_securitie")
    )

    api_prices = get_last_prices_by_tickers(securities)

    for security in securities:
        if security.id_securitie == 36:
            continue

        current_price = api_prices.get(security.ticker)

        if current_price is None:
            current_price = security.quotation

        item = {
            "img": security.icon,
            "name": security.sec_name,
            "short_name": security.ticker,
            "price": fti(current_price),
            "count": fti(portfolio_quantities.get(security.id_securitie, 0)),
            "id": security.catalog_id,
            "id_sec": security.id_securitie,
        }

        data[template[item["id"]]].append(item)

    return data