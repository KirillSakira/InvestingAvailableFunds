from tinkoff.invest import Client
from tinkoff.invest.schemas import CandleInterval
from tinkoff.invest.utils import now
from datetime import timedelta, datetime
from connection import getTokenInvest



CLASS_CODE_MAP = {
    "акции": ["TQBR"],
    "фонды": ["TQTF", "TQIF", "FQBR"],
    "облигации": ["TQOB", "TQCB"],
    "ценные металлы": ["CETS"]
}

def quotation_to_float(quotation):
    return quotation.units + quotation.nano / 1e9

def get_figi(ticker, category):
    if category not in CLASS_CODE_MAP:
        raise ValueError(f"[!] Неизвестная категория: {category}")

    allowed_classes = CLASS_CODE_MAP[category]

    with Client(TOKEN) as client:
        results = client.instruments.find_instrument(query=ticker)

        for instr in results.instruments:
            if (
                instr.ticker.upper() == ticker.upper()
                and instr.class_code in allowed_classes
            ):
                return instr.figi

    return None

TOKEN = getTokenInvest()

def get_candles_by_ticker(ticker, category, interval_option):
    if interval_option == 0:
        interval = CandleInterval.CANDLE_INTERVAL_5_MIN
        from_dt = now() - timedelta(days=3)
    elif interval_option == 1:
        interval = CandleInterval.CANDLE_INTERVAL_1_MIN
        from_dt = now() - timedelta(hours=6)
    elif interval_option == 2:
        interval = CandleInterval.CANDLE_INTERVAL_15_MIN
        from_dt = now() - timedelta(days=7)
    elif interval_option == 3:
        interval = CandleInterval.CANDLE_INTERVAL_HOUR
        from_dt = now() - timedelta(weeks=2)
    elif interval_option == 4:
        interval = CandleInterval.CANDLE_INTERVAL_DAY
        from_dt = now() - timedelta(days=60)

    to_dt = now()

    with Client(TOKEN) as client:
        figi = get_figi(ticker, category)
        if not figi:
            raise ValueError(f"FIGI не найден для тикера {ticker} в категории {category}")

        candles = client.market_data.get_candles(
            figi=figi,
            from_=from_dt,
            to=to_dt,
            interval=interval
        )
        return candles.candles

def get_graph_info_by_interval(ticker, type, interval_option):
    candles = get_candles_by_ticker(ticker, type, interval_option)

    graph_information = []

    for candle in candles:
        graph_point = dict()
        if interval_option == 0:
            graph_point["time_interval"] = candle.time.strftime("%H:%M")
        elif interval_option == 1:
            graph_point["time_interval"] = candle.time.strftime("%H:%M")
        elif interval_option == 2:
            graph_point["time_interval"] = candle.time.strftime("%H:%M")
        elif interval_option == 3:
            graph_point["time_interval"] = int(candle.time.strftime("%H"))
        elif interval_option == 4:
            graph_point["time_interval"] = candle.time.strftime("%d")
        graph_point["time"] = candle.time.strftime("%H:%M %d.%m.%y")
        graph_point["volume"] = str(candle.volume)
        graph_point["price"] = dict()
        graph_point["price"]["open"] = str(quotation_to_float(candle.open))
        graph_point["price"]["high"] = str(quotation_to_float(candle.high))
        graph_point["price"]["low"] = str(quotation_to_float(candle.low))
        graph_point["price"]["close"] = str(quotation_to_float(candle.close))
        graph_point["is_complete"] = str(candle.is_complete)
        graph_information.append(graph_point)

    return graph_information

def get_graph_info(ticker, type):
    result = dict()
    result["5 min"] = get_graph_info_by_interval(ticker, type, 0)
    result["1 min"] = get_graph_info_by_interval(ticker, type, 1)
    result["15 min"] = get_graph_info_by_interval(ticker, type, 2)
    result["1 hour"] = get_graph_info_by_interval(ticker, type, 3)
    result["1 day"] = get_graph_info_by_interval(ticker, type, 4)
    return result

    


