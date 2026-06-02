from app.models import Request
from app.scripts.funcs import fti


def securitiesInfo(securities):
    info = {
        "stocks_data": [],
        "bonds_data": [],
        "funds_data": [],
        "curr_metals_data": [],
    }

    info_indices = {
        1: "stocks_data",
        2: "bonds_data",
        3: "funds_data",
        4: "curr_metals_data",
    }

    for portfolio_security in securities:
        security = portfolio_security.securitie
        total_quantity = portfolio_security.total_quantity

        if security.ticker == "RUB":
            continue

        request = (
            Request.objects
            .filter(securitie=security)
            .order_by("-req_date")
            .first()
        )

        if request is None or request.quantity == 0:
            continue

        old_quotation = request.total_price / request.quantity
        current_quotation = security.quotation
        current_total_price = current_quotation * total_quantity

        securitie_info = {
            "name": security.sec_name,
            "short_name": security.ticker,
            "img": security.icon,
            "price_buy": fti(old_quotation),
            "price_now": fti(current_quotation),
            "price_count_buy": fti(current_total_price),
            "count_buy": fti(total_quantity),
            "price_end": fti((current_quotation - old_quotation) * total_quantity),
            "proc_end": fti((float(current_quotation) / float(old_quotation) - 1) * 100),
        }

        info[info_indices[security.catalog_id]].append(securitie_info)

    return info