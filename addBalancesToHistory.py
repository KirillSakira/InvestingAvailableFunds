import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finportfolio.settings")
django.setup()

from django.db import transaction
from django.utils import timezone

from app.models import BalanceHistory, Portfolio


def main():
    now = timezone.now()

    with transaction.atomic():
        for portfolio in Portfolio.objects.all():
            BalanceHistory.objects.create(
                portfolio=portfolio,
                balance_date=now,
                balance=portfolio.balance,
            )

    print("Balance history updated!")


if __name__ == "__main__":
    main()