from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie
from app.scripts.mainPages.enterprise.securitiesInfo import securitiesInfo


def analyticsPie(request, uid=False):
    try:
        user_id = uid if uid else request.user.id

        pie = {
            "stocks_data": [],
            "bonds_data": [],
            "funds_data": [],
            "curr_metals_data": [],
        }

        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=user_id)
        )

        portfolio = Portfolio.objects.get(
            enterprise=auth_user.legacy_user.enterprise
        )

        securities_qs = (
            PortfolioToSecuritie.objects
            .filter(portfolio=portfolio)
            .select_related("securitie", "securitie__catalog")
        )

        if not securities_qs.exists():
            return pie, {
                "stocks_data": [],
                "bonds_data": [],
                "funds_data": [],
                "curr_metals_data": [],
            }

        securitiesData = securitiesInfo(securities_qs)

        catalog_names = {
            "Акции": "stocks_data",
            "Облигации": "bonds_data",
            "Фонды": "funds_data",
            "Валюта и металлы": "curr_metals_data",
        }

        quantities = {}
        total_sum = 0

        for item in securities_qs:
            security = item.securitie

            if security.ticker == "RUB":
                continue

            securitie_sum = float(item.total_quantity * security.quotation)
            total_sum += securitie_sum

            quantities[security.sec_name] = (
                securitie_sum,
                security.catalog.catalog_name,
                security.icon,
            )

        if total_sum:
            for name, item in quantities.items():
                value, catalog_name, icon = item
                key = catalog_names.get(catalog_name)

                if not key:
                    continue

                pie[key].append(
                    {
                        "name": name,
                        "proc": round(value / total_sum * 100, 2),
                        "count": round(value, 2),
                        "img": icon if icon is not None else "None",
                    }
                )

        for key in ("stocks_data", "bonds_data", "funds_data", "curr_metals_data"):
            pie[key] = sorted(pie[key], key=lambda g: g["name"])
            securitiesData[key] = sorted(securitiesData[key], key=lambda g: g["name"])

        return pie, securitiesData

    except Exception:
        return "Error"