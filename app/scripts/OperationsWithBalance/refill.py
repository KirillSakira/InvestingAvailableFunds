from decimal import Decimal, InvalidOperation

from app.models import AuthUserExtra, Portfolio
from app.scripts.funcs import returnJson, cardValidation
from app.services import create_operation


def refillBack(request):
    try:
        amount = Decimal(request.POST.get("amount") or "0")
    except (InvalidOperation, TypeError):
        return returnJson(data={"amount": "Некорректная сумма перевода"})

    cardNumber = request.POST.get("card_number") or ""
    cardDateInput = request.POST.get("card_date") or ""

    errorsDict = cardValidation(amount, cardNumber, cardDateInput)

    if errorsDict:
        return returnJson(data=errorsDict)

    try:
        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=request.user.id)
        )

        portfolio = Portfolio.objects.get(
            enterprise=auth_user.legacy_user.enterprise
        )

        create_operation(
            portfolio_id=portfolio.id_portfolio,
            oper_type=True,
            amount=amount,
        )

    except Exception:
        return returnJson(status="error", message="Ошибка пополнения")

    return returnJson(status="success", message="Успешное пополнение")