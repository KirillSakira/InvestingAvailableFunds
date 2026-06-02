from app.models import AuthUserExtra, OperationHistory, Portfolio


def _short_name(auth_user):
    name = f"{auth_user.last_name} {auth_user.first_name[0]}."

    if auth_user.patronymic:
        name += f" {auth_user.patronymic[0]}."

    return name


def historyManager(request, uid=False):
    try:
        user_id = uid if uid else request.user.id

        manager_auth = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__employee")
            .get(pk=user_id)
        )

        employee = manager_auth.legacy_user.employee

        portfolios = (
            Portfolio.objects
            .filter(employee=employee)
            .select_related("enterprise")
        )

        data = []

        operation_types = ["Вывод", "Пополнение"]

        for portfolio in portfolios:
            client_auth = (
                AuthUserExtra.objects
                .select_related("legacy_user", "legacy_user__enterprise")
                .get(legacy_user__enterprise=portfolio.enterprise)
            )

            client_name = _short_name(client_auth)

            operations = (
                OperationHistory.objects
                .filter(
                    portfolio=portfolio,
                    oper_status=True,
                )
                .order_by("-oper_date")
            )

            for operation in operations:
                amount = float(operation.amount)

                if amount == int(amount):
                    amount = int(amount)

                data.append(
                    {
                        "id": client_auth.id,
                        "name": client_name,
                        "operation": {
                            "type": operation_types[int(operation.oper_type)],
                            "date": operation.oper_date.strftime("%d.%m.%Y %H:%M"),
                            "price": amount,
                        },
                    }
                )

        return sorted(
            data,
            key=lambda item: item["operation"]["date"],
            reverse=True,
        )

    except Exception:
        return "Error"