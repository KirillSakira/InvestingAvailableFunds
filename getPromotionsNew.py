from tinkoff.invest import Client
from tinkoff.invest.schemas import CandleInterval
from tinkoff.invest.utils import now
from datetime import timedelta

TOKEN = "t.Cw1asA9fD5w6sGKR9XGUPmCBWcFTI7W0WBXfAAAbH-aKW89DeDZSIz9r4AoBiIJvgzFszoUx87s1c4C2I7rroA"

def get_candles_by_ticker(ticker: str, category: str):
    interval = CandleInterval.CANDLE_INTERVAL_5_MIN
    from_dt = now() - timedelta(days=3)

    # interval = CandleInterval.CANDLE_INTERVAL_1_MIN
    # from_dt = now() - timedelta(hours=6)

    # interval = CandleInterval.CANDLE_INTERVAL_15_MIN
    # from_dt = now() - timedelta(days=7)

    # interval = CandleInterval.CANDLE_INTERVAL_HOUR
    # from_dt = now() - timedelta(weeks=2)

    # interval = CandleInterval.CANDLE_INTERVAL_DAY
    # from_dt = now() - timedelta(days=60)

    to_dt = now()

    with Client(TOKEN) as client:
        figi = 'BBG004730N88'
        if not figi:
            raise ValueError(f"FIGI не найден для тикера {ticker} в категории {category}")

        candles = client.market_data.get_candles(
            figi=figi,
            from_=from_dt,
            to=to_dt,
            interval=interval
        )
        return candles.candles

def find_figi_via_search(client: Client, ticker: str, category: str):
    type_map = {
        "shares": "share",
        "bonds": "bond",
        "etfs": "etf",
        "currencies": "currency"
    }

    if category not in type_map:
        raise ValueError(f"Неизвестная категория: {category}")

    results = client.instruments.find_instrument(query=ticker)
    for instr in results.instruments:
        if instr.ticker == ticker and instr.instrument_type == type_map[category]:
            return instr.figi
    return None

# === ПРИМЕР ===
candles = get_candles_by_ticker("SBER", "shares")

for c in candles:
    open_ = c.open.units + c.open.nano / 1e9
    high = c.high.units + c.high.nano / 1e9
    low = c.low.units + c.low.nano / 1e9
    close = c.close.units + c.close.nano / 1e9
    volume = c.volume
    time = c.time
    complete = c.is_complete

    print(f"[{time}] {'✅' if complete else '⏳'} Open: {open_:.2f}, High: {high:.2f}, Low: {low:.2f}, Close: {close:.2f}, Volume: {volume}")