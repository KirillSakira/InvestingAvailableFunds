from connection import connection_db
from app.scripts.funcs import returnJson
from re import sub


def getTradeValue(request):
    fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)
    ticker = request.POST.get('ticker')
    quantity = int(request.POST.get('quantity'))
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select quotation from securities where ticker = \'{ticker}\'')
    cost = dataBase.fetchall()[0][0]
    
    cost *= quantity
    cost = sub(r'\B(?=(\d{3})+(?!\d))', ' ', str(fti(cost)))
    
    return returnJson(status = 'success', message = f'{cost} ₽')