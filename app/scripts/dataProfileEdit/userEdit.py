from django.db import transaction

from app.models import AuthUserExtra, Enterprise
from app.scripts.funcs import check, returnJson


def clientEdit(request):
    email = request.POST.get("email") or ""
    name = request.POST.get("name") or ""
    phone = (request.POST.get("phone") or "").replace("+7", "8")
    address = request.POST.get("address") or ""
    typeProperty = request.POST.get("type_property") or ""
    title = request.POST.get("title") or ""
    idUser = request.POST.get("id") or request.user.id

    errorsDict = {}

    if len(email) > 150:
        errorsDict["email"] = "Почта слишком длинная"

    if len(address) > 150:
        errorsDict["address"] = "Адрес слишком длинный"

    if len(typeProperty) > 50:
        errorsDict["typeProperty"] = "Вид собственности слишком длинный"

    if len(title) > 100:
        errorsDict["title"] = "Наименование организации слишком длинное"

    if check(email, "mail"):
        errorsDict["email"] = "Введите корректную почту"

    if AuthUserExtra.objects.exclude(pk=idUser).filter(email=email).exists():
        errorsDict["email"] = "Данная почта уже используется"

    try:
        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=idUser)
        )
    except AuthUserExtra.DoesNotExist:
        return returnJson(data={"user": "Пользователь не найден"})

    if not auth_user.legacy_user or not auth_user.legacy_user.enterprise_id:
        return returnJson(data={"user": "Клиент не найден"})

    enterprise = auth_user.legacy_user.enterprise

    if not (len(phone) == 11 and phone.isdigit()):
        errorsDict["phone"] = "Телефон введён некорректно"

    if Enterprise.objects.exclude(pk=enterprise.pk).filter(tel=phone).exists():
        errorsDict["phone"] = "Данный номер телефона уже используется"

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict["name"] = "ФИО введён некорректно"
        firstName = ""
        lastName = ""
        patronymic = None
    else:
        lastName, firstName, *args = splitName

        lastName = lastName.capitalize()
        firstName = firstName.capitalize()
        patronymic = args[0].capitalize() if args else None

        if len(firstName) > 150 or len(lastName) > 150 or len(patronymic or "") > 150:
            errorsDict["name"] = "ФИО слишком длинное"

    if errorsDict:
        return returnJson(data=errorsDict)

    with transaction.atomic():
        AuthUserExtra.objects.filter(pk=idUser).update(
            email=email,
            username=email,
            first_name=firstName,
            last_name=lastName,
            patronymic=patronymic,
        )

        Enterprise.objects.filter(pk=enterprise.pk).update(
            tel=phone,
            address=address,
            type_property=typeProperty,
            title=title,
        )

    return returnJson(status="success", message="Данные обновлены")