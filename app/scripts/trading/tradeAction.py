from app.models import AuthUserExtra, Portfolio, PortfolioToSecuritie, Queue, Security
from app.scripts.funcs import returnJson, fti
from app.services import create_request

RUB_SECURITY_ID = 36


def getAdditionalInfo(security, portfolio):
    link = (
        PortfolioToSecuritie.objects
        .filter(portfolio=portfolio, securitie=security)
        .first()
    )

    if not link:
        return [0, 0]

    quotation = security.quotation
    portfolio_price = fti(link.total_quantity) * fti(quotation)

    first_queue_item = (
        Queue.objects
        .filter(portfolio=portfolio, securitie=security)
        .order_by("queue_date")
        .first()
    )

    if first_queue_item and quotation:
        old_price = first_queue_item.quotation
        proc = 100 - (float(old_price) / float(quotation)) * 100
    else:
        proc = 0

    return [portfolio_price, proc]


def _get_portfolio_by_user_id(user_id):
    auth_user = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .get(pk=user_id)
    )

    return Portfolio.objects.get(
        enterprise=auth_user.legacy_user.enterprise
    )


def tradeAction(request):
    ticker = request.POST.get("ticker")
    user_id = request.POST.get("uid") or request.user.id

    try:
        action = bool(int(request.POST.get("action")))
    except (TypeError, ValueError):
        return returnJson(status="error", message="Некорректное действие")

    try:
        quantity = int(request.POST.get("quantity") or "0")
    except (TypeError, ValueError):
        return returnJson(status="error", message="Введите количество")

    if quantity <= 0:
        return returnJson(status="error", message="Введите количество")

    try:
        security = Security.objects.get(ticker=ticker)
        portfolio = _get_portfolio_by_user_id(user_id)

        request_obj = create_request(
            portfolio_id=portfolio.id_portfolio,
            securitie_id=security.id_securitie,
            req_type=action,
            quantity=quantity,
        )

        if not request_obj.req_status:
            if action:
                return returnJson(status="error", message="Недостаточно свободных средств")

            return returnJson(status="error", message="Указано неверное колличество для продажи")

        security_link = (
            PortfolioToSecuritie.objects
            .filter(portfolio=portfolio, securitie=security)
            .first()
        )

        rub_link = (
            PortfolioToSecuritie.objects
            .filter(portfolio=portfolio, securitie_id=RUB_SECURITY_ID)
            .first()
        )

        new_total_quantity = security_link.total_quantity if security_link else 0
        new_balance = rub_link.total_quantity if rub_link else 0
        info = getAdditionalInfo(security, portfolio) if new_total_quantity > 0 else [0, 0]

        return returnJson(
            data={
                "total_quantity": fti(new_total_quantity),
                "balance": fti(new_balance),
                "status": "success",
                "message": "Покупка совершена успешно" if action else "Продажа совершена успешно",
                "total_sum": info[0],
                "proc": info[1],
            }
        )

    except Security.DoesNotExist:
        return returnJson(status="error", message="Инструмент не найден")
    except Exception:
        return returnJson(status="error", message="Ошибка совершения сделки")