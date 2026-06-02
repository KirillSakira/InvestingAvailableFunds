from app.models import AuthUserExtra


def private_profile(request, id=None):
    try:
        user_id = id if id is not None else request.user.id

        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=user_id)
        )

        enterprise = auth_user.legacy_user.enterprise

        patronymic = auth_user.patronymic or ""

        return {
            "email": auth_user.email,
            "name": f"{auth_user.last_name} {auth_user.first_name} {patronymic}".strip(),
            "phone": enterprise.tel,
            "address": enterprise.address,
            "type_property": enterprise.type_property,
            "title": enterprise.title,
        }

    except Exception:
        return "Error"