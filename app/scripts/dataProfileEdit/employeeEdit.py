from django.db import transaction

from app.models import AuthUserExtra
from app.scripts.funcs import check, returnJson


def employeeEdit(request):
    user_id = request.POST.get("id") or request.user.id
    email = request.POST.get("email") or ""
    name = request.POST.get("name") or ""

    errorsDict = {}

    if len(email) > 150:
        errorsDict["email"] = "Почта слишком длинная"

    if check(email, "mail"):
        errorsDict["email"] = "Введите корректную почту"

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict["name"] = "ФИО введён некорректно"
        first_name = ""
        last_name = ""
        patronymic = None
    else:
        last_name, first_name, *args = splitName

        last_name = last_name.capitalize()
        first_name = first_name.capitalize()
        patronymic = args[0].capitalize() if args else None

        if len(first_name) > 150 or len(last_name) > 150 or len(patronymic or "") > 150:
            errorsDict["name"] = "ФИО слишком длинное"

    if errorsDict:
        return returnJson(data=errorsDict)

    with transaction.atomic():
        AuthUserExtra.objects.filter(pk=user_id).update(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )

    return returnJson(status="success", message="Данные обновлены")