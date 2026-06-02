from decimal import Decimal, InvalidOperation

from app.front_app.viewBack.getUserData import getUserData
from app.models import AuthUserExtra, Portfolio
from app.scripts.funcs import returnJson, cardValidation
from app.services import create_operation


def withdrawBack(request):
    try:
        amount = Decimal(request.POST.get("amount") or "0")
    except (InvalidOperation, TypeError):
        return returnJson(data={"amount": "Некорректная сумма перевода"})

    cardNumber = request.POST.get("card_number") or ""

    errorsDict = cardValidation(amount, cardNumber)

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

        operation = create_operation(
            portfolio_id=portfolio.id_portfolio,
            oper_type=False,
            amount=amount,
        )

        if not operation.oper_status:
            return returnJson(data={"message": "Недостаточно свободных средств"})

    except Exception:
        return returnJson(status="error", message="Ошибка снятия")

    userData = getUserData(request)

    return returnJson(
        data={
            "status": "success",
            "message": "Успешное снятие",
            "balance": f"{userData['balance']} ₽",
        }
    )