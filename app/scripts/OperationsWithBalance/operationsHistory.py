from app.models import AuthUserExtra, OperationHistory, Portfolio


def _short_name(auth_user):
    name = f"{auth_user.last_name} {auth_user.first_name[0]}."

    if auth_user.patronymic:
        name += f" {auth_user.patronymic[0]}."

    return name


def history(request, uid=False):
    try:
        user_id = uid if uid else request.user.id
        name = ""

        auth_user = (
            AuthUserExtra.objects
            .select_related("legacy_user", "legacy_user__enterprise")
            .get(pk=user_id)
        )

        if uid:
            name = _short_name(auth_user)

        portfolio = Portfolio.objects.get(
            enterprise=auth_user.legacy_user.enterprise
        )

        operations = (
            OperationHistory.objects
            .filter(
                portfolio=portfolio,
                oper_status=True,
            )
            .order_by("-oper_date")
        )

        data = []

        operation_types = ["Вывод", "Пополнение"]

        for operation in operations:
            operation_amount = float(operation.amount)

            if operation_amount == int(operation_amount):
                operation_amount = int(operation_amount)

            data.append(
                {
                    "type": operation_types[int(operation.oper_type)],
                    "date": operation.oper_date.strftime("%d.%m.%Y %H:%M"),
                    "price": operation_amount,
                }
            )

        return [name, data]

    except Exception:
        return ["", "Error"]