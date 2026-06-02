from app.models import AuthUserExtra


def _short_fio(user):
    first_initial = f"{user.first_name[0]}." if user.first_name else ""
    patronymic_initial = f" {user.patronymic[0]}." if user.patronymic else ""

    return f"{user.last_name} {first_initial}{patronymic_initial}".strip()


def adminMainPage():
    clients_qs = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__enterprise")
        .filter(
            legacy_user__employee__isnull=True,
            legacy_user__enterprise__isnull=False,
        )
    )

    employees_qs = (
        AuthUserExtra.objects
        .select_related("legacy_user", "legacy_user__employee", "legacy_user__employee__post")
        .filter(
            legacy_user__enterprise__isnull=True,
            legacy_user__employee__post_id=2,
        )
    )

    clientsData = [
        {
            "id": user.id,
            "fio": _short_fio(user),
        }
        for user in clients_qs
    ]

    employeesData = [
        {
            "id": user.id,
            "fio": _short_fio(user),
        }
        for user in employees_qs
    ]

    return {
        "clients": clientsData,
        "employees": employeesData,
    }