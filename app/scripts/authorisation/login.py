from django.contrib.auth import authenticate, login

from app.scripts.funcs import returnJson


def authorisationBack(request):
    if request.method != "POST":
        return returnJson(status="Error", message="Метод не поддерживается")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is not None:
        login(request, user)
        return returnJson(status="success")

    return returnJson(status="Error", message="Неверный логин или пароль")