from tinkoff.invest import Client, RequestError
import psycopg2

f = open('token.txt', 'r')
TOKEN = f.read()
f.close()

connection = psycopg2.connect("dbname=test7 user=postgres password=1234 host=localhost port=5432")
dataBase = connection.cursor()

dataBase.execute('select s.ticker, c.catalog_name from securities s join catalogs c on s.id_catalog = c.id_catalog;')
tickersBase = dataBase.fetchall()

tickers = {
    "Акции": [],
    "Облигации": [],
    "Фонды": [],
    "Валюта и металлы": []
}

for row in tickersBase:
    if row[0] != 'RUB':
        tickers[row[1]].append(row[0])

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
        for instrument in instruments:
            if instrument.ticker == ticker:
                return instrument.figi
        print(f"No FIGI found for ticker: {ticker}")
        return None
    except RequestError as e:
        print(f"Could not retrieve FIGI for {ticker}: {e}")
        return None
    
# Функция для получения текущей цены по FIGI
def getCurrentPrice(client, figi):
    try:
        response = client.market_data.get_last_prices(figi=[figi])
        if response.last_prices:
            return response.last_prices[0].price
        else:
            print(f"No price data found for FIGI {figi}")
            return None
    except RequestError as e:
        print(f"Could not retrieve price for FIGI {figi}: {e}")
        return None
    
# Основной блок
with Client(TOKEN) as client:
    for asset_type, tickerList in tickers.items():
        for ticker in tickerList:
            figi = getFigiByTicker(client, ticker, asset_type)
            if figi:
                currentPrice = getCurrentPrice(client, figi)
                if current_price:
                    print(f"Current price for {ticker} (FIGI: {figi}): {currentPrice.units}.{str(currentPrice.nano)} RUB")
                    current_price = float(f'{currentPrice.units}.{str(currentPrice.nano)}')
                    dataBase.execute(f"update securities set quotation = {currentPrice} where ticker = '{ticker}'")
connection.commit()
dataBase.close()
connection.close()