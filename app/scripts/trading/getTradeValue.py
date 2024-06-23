from connection import connection_db
from app.scripts.funcs import returnJson


def getTradeValue(request):
    ticker = request.POST.get('ticker')
    quantity = request.POST.get('quantity')
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select quotation form securities where ticker = {ticker}')
    cost = dataBase.fetchall()[0][0]
    
    cost *= quantity
    
    return returnJson(status = 'success', message = cost)