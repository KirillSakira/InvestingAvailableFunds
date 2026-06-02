from app.models import AuthUserExtra


def manager_profile(request, id=None):
    try:
        user_id = id if id is not None else request.user.id

        auth_user = AuthUserExtra.objects.get(pk=user_id)

        name = f"{auth_user.last_name} {auth_user.first_name}"

        if auth_user.patronymic:
            name += f" {auth_user.patronymic}"

        return {
            "email": auth_user.email,
            "name": name,
        }

    except Exception:
        return "Error"