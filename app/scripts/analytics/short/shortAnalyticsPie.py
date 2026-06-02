from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie


def shortAnalyticsPie(request, uid=False):
    try:
        colors = {
            "Акции": "#634FED",
            "Облигации": "#3AA1FF",
            "Фонды": "#FF523A",
            "Валюта и металлы": "#F1EDFD",
        }

        user_id = uid if uid else request.user.id

        auth_user = AuthUserExtra.objects.select_related("legacy_user").get(pk=user_id)

        portfolio = Portfolio.objects.get(
            enterprise__legacy_user=auth_user.legacy_user
        )

        securities = (
            PortfolioToSecuritie.objects
            .filter(portfolio=portfolio)
            .select_related("securitie", "securitie__catalog")
        )

        quantities = {}
        total_sum = 0

        for item in securities:
            security = item.securitie

            if security.ticker == "RUB":
                continue

            catalog_name = security.catalog.catalog_name
            securitie_quantity = float(item.total_quantity * security.quotation)

            total_sum += securitie_quantity
            quantities[catalog_name] = securitie_quantity + quantities.get(catalog_name, 0)

        graph_pie = []

        if total_sum:
            for catalog_name, value in quantities.items():
                graph_pie.append(
                    {
                        "name": catalog_name,
                        "proc": round(value / total_sum * 100, 2),
                        "count": round(value, 2),
                        "color": colors.get(catalog_name, "#000000"),
                    }
                )

        return graph_pie

    except Exception:
        return "Error", ""