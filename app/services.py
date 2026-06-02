from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone

from .models import (
    Portfolio,
    Security,
    PortfolioToSecuritie,
    Queue,
    Request,
    OperationHistory,
)

FUNDS_SECURITY_ID = 36
COMMISSION_RATE = Decimal("0.2504")


def _pts_qs(portfolio_id, securitie_id):
    return PortfolioToSecuritie.objects.filter(
        portfolio_id=portfolio_id,
        securitie_id=securitie_id,
    )


def _recalculate_avg_quotation(portfolio_id: int, securitie_id: int) -> None:
    total_expr = ExpressionWrapper(
        F("quantity") * F("quotation"),
        output_field=DecimalField(max_digits=30, decimal_places=5),
    )

    agg = Queue.objects.filter(
        portfolio_id=portfolio_id,
        securitie_id=securitie_id,
    ).aggregate(
        total_sum=Sum(total_expr),
        total_qty=Sum("quantity"),
    )

    total_qty = agg["total_qty"]

    if total_qty:
        _pts_qs(portfolio_id, securitie_id).update(
            avg_quotation=agg["total_sum"] / Decimal(total_qty)
        )


def _get_or_create_funds_row(portfolio_id):
    row = _pts_qs(portfolio_id, FUNDS_SECURITY_ID).select_for_update().first()

    if row is None:
        row = PortfolioToSecuritie.objects.create(
            portfolio_id=portfolio_id,
            securitie_id=FUNDS_SECURITY_ID,
            total_quantity=0,
            avg_quotation=1,
        )

    return row


@transaction.atomic
def create_operation(*, portfolio_id: int, oper_type: bool, amount: Decimal, oper_date=None) -> OperationHistory:
    oper_date = oper_date or timezone.now()

    portfolio = Portfolio.objects.select_for_update().get(pk=portfolio_id)
    funds_row = _get_or_create_funds_row(portfolio_id)

    oper_status = True

    if oper_type:
        portfolio.deposition += amount
        portfolio.balance += amount
        portfolio.save(update_fields=["deposition", "balance"])

        _pts_qs(portfolio_id, FUNDS_SECURITY_ID).update(
            total_quantity=funds_row.total_quantity + amount
        )

    else:
        if amount <= funds_row.total_quantity:
            portfolio.deposition -= amount
            portfolio.balance -= amount
            portfolio.save(update_fields=["deposition", "balance"])

            _pts_qs(portfolio_id, FUNDS_SECURITY_ID).update(
                total_quantity=funds_row.total_quantity - amount
            )
        else:
            oper_status = False

    return OperationHistory.objects.create(
        portfolio_id=portfolio_id,
        oper_type=oper_type,
        oper_status=oper_status,
        oper_date=oper_date,
        amount=amount,
    )


@transaction.atomic
def create_request(*, portfolio_id: int, securitie_id: int, req_type: bool, quantity: int, req_date=None) -> Request:
    req_date = req_date or timezone.now()
    quantity = int(quantity)

    portfolio = Portfolio.objects.select_for_update().get(pk=portfolio_id)
    security = Security.objects.get(pk=securitie_id)

    quotation = security.quotation
    total_price = Decimal(quantity) * quotation

    req_status = True
    commission = Decimal("0")

    funds_row = _get_or_create_funds_row(portfolio_id)

    if req_type:
        if total_price <= funds_row.total_quantity:
            pos = _pts_qs(portfolio_id, securitie_id).select_for_update().first()

            if pos is None:
                PortfolioToSecuritie.objects.create(
                    portfolio_id=portfolio_id,
                    securitie_id=securitie_id,
                    total_quantity=quantity,
                    avg_quotation=quotation,
                )
            else:
                _pts_qs(portfolio_id, securitie_id).update(
                    total_quantity=pos.total_quantity + Decimal(quantity)
                )

            _pts_qs(portfolio_id, FUNDS_SECURITY_ID).update(
                total_quantity=funds_row.total_quantity - total_price
            )

            Queue.objects.create(
                portfolio_id=portfolio_id,
                securitie_id=securitie_id,
                queue_date=req_date,
                quantity=quantity,
                quotation=quotation,
            )

            _recalculate_avg_quotation(portfolio_id, securitie_id)
        else:
            req_status = False

    else:
        pos = _pts_qs(portfolio_id, securitie_id).select_for_update().first()
        total_quant = pos.total_quantity if pos else Decimal("0")

        if Decimal(quantity) <= total_quant:
            remaining = quantity
            cost_basis_sum = Decimal("0")

            lots = list(
                Queue.objects
                .select_for_update()
                .filter(
                    portfolio_id=portfolio_id,
                    securitie_id=securitie_id,
                )
                .order_by("queue_date")
            )

            for lot in lots:
                if remaining == 0:
                    break

                lot_filter = Queue.objects.filter(
                    portfolio_id=portfolio_id,
                    securitie_id=securitie_id,
                    queue_date=lot.queue_date,
                )

                if remaining >= lot.quantity:
                    remaining -= lot.quantity
                    cost_basis_sum += Decimal(lot.quantity) * lot.quotation
                    lot_filter.delete()
                else:
                    cost_basis_sum += Decimal(remaining) * lot.quotation
                    lot_filter.update(quantity=lot.quantity - remaining)
                    remaining = 0

            commission = (total_price - cost_basis_sum) * COMMISSION_RATE

            if Decimal(quantity) == total_quant:
                _pts_qs(portfolio_id, securitie_id).delete()
            else:
                _pts_qs(portfolio_id, securitie_id).update(
                    total_quantity=pos.total_quantity - Decimal(quantity)
                )
                _recalculate_avg_quotation(portfolio_id, securitie_id)

            _pts_qs(portfolio_id, FUNDS_SECURITY_ID).update(
                total_quantity=funds_row.total_quantity + total_price - commission
            )
        else:
            req_status = False

    return Request.objects.create(
        portfolio_id=portfolio_id,
        securitie_id=securitie_id,
        req_type=req_type,
        req_status=req_status,
        quantity=quantity,
        req_date=req_date,
        commission=commission,
        total_price=total_price,
        employee_id=portfolio.employee_id or 1,
    )