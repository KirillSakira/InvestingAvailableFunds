from random import randint as rnd

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction

from app.models import (
    AuthUserExtra,
    Employee,
    Enterprise,
    LegacyUser,
    Portfolio,
    PortfolioToSecuritie,
    Security,
)
from app.scripts.funcs import returnJson, checkPass, check


def isClient(role):
    return role in ["Admin", "Manager"]


def generate_account_number():
    return rnd(int("1" + "0" * 19), int("9" * 20))


def registrationBack(request):
    role = request.POST.get("role")
    username = request.POST.get("login")
    password = request.POST.get("password") or ""
    name = request.POST.get("name") or ""
    email = request.POST.get("email") or ""
    phone = request.POST.get("phone") or ""
    address = request.POST.get("address") or ""
    title = request.POST.get("title") or ""
    typeProperty = request.POST.get("typeProperty") or ""

    if username is None:
        username = email

    errorsDict = {}

    if isClient(role):
        address = ""
        title = ""
        typeProperty = ""
    else:
        if role is None and typeProperty is None:
            errorsDict["role"] = "Выберите роль"
            return returnJson(data=errorsDict)

    if len(email) > 150:
        errorsDict["email"] = "Почта слишком длинная"

    if len(address) > 150:
        errorsDict["address"] = "Адрес слишком длинный"

    if len(title) > 100:
        errorsDict["title"] = "Название организации слишком длинное"

    if len(typeProperty) > 50:
        errorsDict["typeProperty"] = "Тип собственности слишком длинный"

    if len(password) < 8:
        errorsDict["password"] = "Пароль слишком короткий"

    if checkPass(password):
        errorsDict["password"] = "Пароль имеет недопустимые символы"

    if User.objects.filter(username=username).exists():
        errorsDict["email"] = "Пользователь уже существует"

    if check(email, "mail"):
        errorsDict["email"] = "Введите корректную почту"

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict["name"] = "ФИО введён некорректно"
        first_name = ""
        last_name = ""
        patronymic = ""
    else:
        last_name, first_name, *args = splitName

        last_name = last_name.capitalize()
        first_name = first_name.capitalize()
        patronymic = args[0].capitalize() if args else ""

        if len(first_name) > 150 or len(last_name) > 150 or len(patronymic) > 150:
            errorsDict["name"] = "ФИО слишком длинное"

    if not isClient(role):
        phone = phone.replace("+7", "8")

        if not (len(phone) == 11 and phone.isdigit()):
            errorsDict["phone"] = "Телефон введён некорректно"

        if Enterprise.objects.filter(tel=phone).exists():
            errorsDict["phone"] = "Телефон уже используется"

        if address.replace(" ", "") == "":
            errorsDict["address"] = "Введите адрес"

        if title.replace(" ", "") == "":
            errorsDict["title"] = "Введите название компании"

        if typeProperty.replace(" ", "") == "":
            errorsDict["typeProperty"] = "Введите тип собственности"

    if errorsDict:
        return returnJson(data=errorsDict)

    with transaction.atomic():
        employee = None
        enterprise = None

        if not isClient(role):
            enterprise = Enterprise.objects.create(
                title=title,
                type_property=typeProperty,
                address=address,
                tel=phone,
            )

            accountNumber = generate_account_number()

            while Portfolio.objects.filter(account_number=accountNumber).exists():
                accountNumber = generate_account_number()

            portfolio = Portfolio.objects.create(
                balance=0,
                deposition=0,
                account_number=accountNumber,
                enterprise=enterprise,
            )

            rub_security = Security.objects.get(id_securitie=36)

            PortfolioToSecuritie.objects.create(
                portfolio=portfolio,
                securitie=rub_security,
                total_quantity=0,
                avg_quotation=1,
            )

        else:
            if role == "Admin":
                employee = Employee.objects.create(post_id=1)
            elif role == "Manager":
                employee = Employee.objects.create(post_id=2)

        legacy_user = LegacyUser.objects.create(
            employee=employee,
            enterprise=enterprise,
        )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        AuthUserExtra.objects.filter(pk=user.pk).update(
            legacy_user=legacy_user,
            patronymic=patronymic or None,
        )

        if not isClient(role):
            auth_user = authenticate(
                request,
                username=username,
                password=password,
            )
            login(request, auth_user)

    return returnJson(status="success")