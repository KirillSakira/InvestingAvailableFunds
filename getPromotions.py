import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finportfolio.settings")
django.setup()

from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from tinkoff.invest import Client, RequestError

from connection import getTokenInvest
from app.models import Security, Portfolio, PortfolioToSecuritie


TOKEN = getTokenInvest()


def quotation_to_decimal(price):
    return Decimal(price.units) + Decimal(price.nano) / Decimal("1000000000")


def getFigiByTicker(client, ticker, assetType):
    try:
        if assetType == "Акции":
            instruments = client.instruments.shares().instruments
        elif assetType == "Облигации":
            instruments = client.instruments.bonds().instruments
        elif assetType == "Фонды":
            instruments = client.instruments.etfs().instruments
        elif assetType == "Валюта и металлы":
            instruments = client.instruments.currencies().instruments
        else:
            return None

        for instrument in instruments:
            if instrument.ticker == ticker:
                return instrument.figi

        print(f"No FIGI found for ticker: {ticker}")
        return None

    except RequestError as e:
        print(f"Could not retrieve FIGI for {ticker}: {e}")
        return None


def getCurrentPrice(client, figi):
    try:
        response = client.market_data.get_last_prices(figi=[figi])

        if response.last_prices:
            return response.last_prices[0].price

        print(f"No price data found for FIGI {figi}")
        return None

    except RequestError as e:
        print(f"Could not retrieve price for FIGI {figi}: {e}")
        return None


def update_balances():
    total_expr = ExpressionWrapper(
        F("total_quantity") * F("securitie__quotation"),
        output_field=DecimalField(max_digits=30, decimal_places=5),
    )

    portfolio_sums = (
        PortfolioToSecuritie.objects
        .values("portfolio_id")
        .annotate(total_balance=Sum(total_expr))
    )

    for item in portfolio_sums:
        Portfolio.objects.filter(pk=item["portfolio_id"]).update(
            balance=item["total_balance"] or 0
        )


def main():
    securities = (
        Security.objects
        .select_related("catalog")
        .exclude(ticker="RUB")
        .order_by("id_securitie")
    )

    with Client(TOKEN) as client:
        with transaction.atomic():
            for security in securities:
                asset_type = security.catalog.catalog_name
                ticker = security.ticker

                figi = getFigiByTicker(client, ticker, asset_type)

                if not figi:
                    continue

                current_price = getCurrentPrice(client, figi)

                if not current_price:
                    continue

                price = quotation_to_decimal(current_price)

                print(f"Current price for {ticker} (FIGI: {figi}): {price} RUB")

                Security.objects.filter(pk=security.pk).update(
                    quotation=price
                )

            update_balances()

    print("Balances updated!")


if __name__ == "__main__":
    main()