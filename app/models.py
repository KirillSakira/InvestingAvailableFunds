from django.db import models
from django.utils import timezone


class AdditionalInfo(models.Model):
    id_add_info = models.SmallAutoField(primary_key=True, db_column="id_add_info")
    yield_close = models.CharField(max_length=20)
    closing_date = models.DateTimeField()
    coupon_payment_date = models.DateTimeField()
    coupon = models.CharField(max_length=50)
    coupon_value = models.DecimalField(max_digits=20, decimal_places=5)
    nominal = models.DecimalField(max_digits=20, decimal_places=5)
    number_payments_per_year = models.BigIntegerField()
    depreciation = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "additional_info"


class Catalog(models.Model):
    id_catalog = models.SmallAutoField(primary_key=True, db_column="id_catalog")
    catalog_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "catalogs"

    def __str__(self):
        return self.catalog_name


class Post(models.Model):
    id_post = models.SmallAutoField(primary_key=True, db_column="id_post")
    post_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = "posts"

    def __str__(self):
        return self.post_name


class Employee(models.Model):
    id_employee = models.SmallAutoField(primary_key=True, db_column="id_employee")
    post = models.ForeignKey(Post, models.DO_NOTHING, db_column="id_post")

    class Meta:
        managed = False
        db_table = "employees"

    def __str__(self):
        return f"Employee #{self.id_employee}"


class Enterprise(models.Model):
    id_enterprise = models.SmallAutoField(primary_key=True, db_column="id_enterprise")
    title = models.CharField(max_length=100)
    type_property = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    tel = models.CharField(max_length=11, unique=True)

    class Meta:
        managed = False
        db_table = "enterprises"

    def __str__(self):
        return self.title


class LegacyUser(models.Model):
    id_user = models.SmallAutoField(primary_key=True, db_column="id_user")
    employee = models.OneToOneField(
        Employee,
        models.DO_NOTHING,
        db_column="id_employee",
        blank=True,
        null=True,
        related_name="legacy_user",
    )
    enterprise = models.OneToOneField(
        Enterprise,
        models.DO_NOTHING,
        db_column="id_enterprise",
        blank=True,
        null=True,
        related_name="legacy_user",
    )

    class Meta:
        managed = False
        db_table = "users"
        constraints = [
            models.CheckConstraint(
                name="user_check_is_null",
                check=(
                    (models.Q(employee__isnull=True) | models.Q(enterprise__isnull=True))
                    & (models.Q(employee__isnull=False) | models.Q(enterprise__isnull=False))
                ),
            )
        ]

    def __str__(self):
        return f"LegacyUser #{self.id_user}"


class AuthUserExtra(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField(default=timezone.now)

    legacy_user = models.ForeignKey(
        LegacyUser,
        models.DO_NOTHING,
        db_column="id_user",
        blank=True,
        null=True,
        related_name="auth_accounts",
        db_constraint=False,
    )
    patronymic = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auth_user"

    def __str__(self):
        return self.username


def get_auth_extra_for_django_user(user):
    return AuthUserExtra.objects.select_related("legacy_user").get(pk=user.pk)


class Portfolio(models.Model):
    id_portfolio = models.SmallAutoField(primary_key=True, db_column="id_portfolio")
    balance = models.DecimalField(max_digits=20, decimal_places=5)
    employee = models.ForeignKey(
        Employee,
        models.DO_NOTHING,
        db_column="id_employee",
        blank=True,
        null=True,
        related_name="portfolios",
    )
    deposition = models.DecimalField(max_digits=20, decimal_places=5)
    account_number = models.DecimalField(max_digits=21, decimal_places=0, unique=True)
    enterprise = models.ForeignKey(
        Enterprise,
        models.DO_NOTHING,
        db_column="id_enterprise",
        related_name="portfolios",
    )

    class Meta:
        managed = False
        db_table = "portfolios"

    def __str__(self):
        return f"Portfolio #{self.id_portfolio}"


class Security(models.Model):
    id_securitie = models.SmallAutoField(primary_key=True, db_column="id_securitie")
    sec_name = models.CharField(max_length=100, unique=True)
    ticker = models.CharField(max_length=100, unique=True)
    quotation = models.DecimalField(max_digits=15, decimal_places=5)
    catalog = models.ForeignKey(
        Catalog,
        models.DO_NOTHING,
        db_column="id_catalog",
        related_name="securities",
    )
    description = models.TextField(blank=True, null=True)
    add_info = models.ForeignKey(
        AdditionalInfo,
        models.DO_NOTHING,
        db_column="id_add_info",
        blank=True,
        null=True,
        related_name="securities",
    )
    icon = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "securities"

    def __str__(self):
        return f"{self.sec_name} ({self.ticker})"


class PortfolioToSecuritie(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        models.DO_NOTHING,
        db_column="id_portfolio",
        primary_key=True,
        related_name="securities_links",
    )
    securitie = models.ForeignKey(
        Security,
        models.DO_NOTHING,
        db_column="id_securitie",
        related_name="portfolio_links",
    )
    total_quantity = models.DecimalField(max_digits=20, decimal_places=5)
    avg_quotation = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        managed = False
        db_table = "portfolio_to_securitie"
        unique_together = (("portfolio", "securitie"),)


class Queue(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        models.DO_NOTHING,
        db_column="id_portfolio",
        primary_key=True,
        related_name="queue_items",
    )
    securitie = models.ForeignKey(
        Security,
        models.DO_NOTHING,
        db_column="id_securitie",
        related_name="queue_items",
    )
    queue_date = models.DateTimeField()
    quantity = models.BigIntegerField()
    quotation = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        managed = False
        db_table = "queue"
        unique_together = (("portfolio", "securitie", "queue_date"),)
        ordering = ["queue_date"]


class Request(models.Model):
    id_request = models.AutoField(primary_key=True, db_column="id_request")
    portfolio = models.ForeignKey(
        Portfolio,
        models.DO_NOTHING,
        db_column="id_portfolio",
        related_name="requests",
    )
    securitie = models.ForeignKey(
        Security,
        models.DO_NOTHING,
        db_column="id_securitie",
        related_name="requests",
    )
    req_type = models.BooleanField()
    req_status = models.BooleanField(default=True)
    quantity = models.BigIntegerField()
    req_date = models.DateTimeField(default=timezone.now)
    commission = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    total_price = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    employee = models.ForeignKey(
        Employee,
        models.DO_NOTHING,
        db_column="id_employee",
        default=1,
        related_name="requests",
    )

    class Meta:
        managed = False
        db_table = "requests"


class OperationHistory(models.Model):
    id_operation = models.AutoField(primary_key=True, db_column="id_operation")
    oper_type = models.BooleanField()
    oper_status = models.BooleanField(default=True)
    oper_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    portfolio = models.ForeignKey(
        Portfolio,
        models.DO_NOTHING,
        db_column="id_portfolio",
        related_name="operations",
    )

    class Meta:
        managed = False
        db_table = "operations_history"


class BalanceHistory(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        models.DO_NOTHING,
        db_column="id_portfolio",
        primary_key=True,
        related_name="balance_history",
    )
    balance_date = models.DateTimeField(default=timezone.now)
    balance = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        managed = False
        db_table = "balances_history"
        unique_together = (("portfolio", "balance_date"),)
        ordering = ["balance_date"]


class Message(models.Model):
    id_message = models.AutoField(primary_key=True, db_column="id_message")
    sender = models.ForeignKey(
        LegacyUser,
        models.DO_NOTHING,
        db_column="id_sender",
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        LegacyUser,
        models.DO_NOTHING,
        db_column="id_receiver",
        related_name="received_messages",
    )
    message_date = models.DateTimeField(default=timezone.now)
    message_content = models.TextField()

    class Meta:
        managed = False
        db_table = "messages"
        ordering = ["message_date"]