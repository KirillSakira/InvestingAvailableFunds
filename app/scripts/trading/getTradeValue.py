from app.models import Security
from app.scripts.funcs import returnJson, fti, numFormat


def getTradeValue(request):
    ticker = request.POST.get("ticker")

    try:
        quantity = int(request.POST.get("quantity") or 0)
    except ValueError:
        return returnJson(status="error", message="Некорректное количество")

    try:
        security = Security.objects.get(ticker=ticker)
    except Security.DoesNotExist:
        return returnJson(status="error", message="Инструмент не найден")

    cost = security.quotation * quantity
    cost = numFormat(fti(cost))

    return returnJson(status="success", message=f"{cost} ₽")