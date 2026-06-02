from datetime import datetime as dt
from json import dumps
from re import fullmatch, sub

from django.http import HttpResponse


def fti(value):
    value = float(round(value, 2))
    return int(value) if value == int(value) else value


def check(string, param):
    patterns = {
        "mail": r"^[\w\d._%+-]+@[\w\d.-]+\.[A-Za-z]{2,}$",
    }

    value = string or ""
    return fullmatch(patterns[param], value) is None


def numFormat(num):
    return sub(r"\B(?=(\d{3})+(?!\d))", " ", str(num))


def checkPass(password):
    password = password or ""

    available_symbols = [i for i in range(48, 58)]
    available_symbols.extend([i for i in range(97, 123)])

    return list(
        filter(
            lambda symbol: ord(symbol) not in available_symbols,
            list(password.lower()),
        )
    ) != []


def returnJson(data=None, status="", message=""):
    if data is None:
        data = {}

    if data == {}:
        response_data = {
            "status": status,
            "message": message,
        }
    else:
        response_data = data

    return HttpResponse(
        dumps(response_data, ensure_ascii=False),
        content_type="application/json",
    )


def cardValidation(amount, cardNumber, cardDate=""):
    errorsDict = {}

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        errorsDict["amount"] = "Некорректная сумма перевода"
        amount = 0

    cardNumber = str(cardNumber or "").replace(" ", "")
    cardDate = str(cardDate or "")

    if amount <= 0:
        errorsDict["amount"] = "Некорректная сумма перевода"

    if len(cardNumber) != 16 or not cardNumber.isdigit():
        errorsDict["card_number"] = "Некорректный номер карты"

    if cardDate != "":
        card_date_flag = False

        try:
            if "/" in cardDate:
                month, year = cardDate.split("/")
            elif "." in cardDate:
                month, year = cardDate.split(".")
            else:
                month, year = cardDate[:2], cardDate[2:]

            month = int(month)
            year = int(year)

            if year < 100:
                year += 2000

            if month not in range(1, 13):
                card_date_flag = True
            else:
                card_date = dt.strptime(f"{year}/{month}/01", "%Y/%m/%d")
                today_month = dt(dt.today().year, dt.today().month, 1)

                if card_date < today_month:
                    card_date_flag = True

        except Exception:
            card_date_flag = True

        if card_date_flag:
            errorsDict["card_date"] = (
                "Карта недействительна или некорректный срок действия карты"
            )

    return errorsDict