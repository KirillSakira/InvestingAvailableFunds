from connection import connection_db


def getSecuritieInfo(request, userId, idSecuritie): 
    fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_user from auth_user where id={userId}')
    idUser = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={idUser}')
    idPortfolio = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'select sec_name, quotation from securities where id_securitie={idSecuritie}')
    security = dataBase.fetchall()[0]
    
    dataBase.execute(f'select quotation from queue where id_security={idSecuritie} and id_portfolio={idPortfolio} order by queue_date')
    oldPrice = dataBase.fetchall()[0][0]
    
    newPrice = security[1]
    proc = 100 - (float(oldPrice)/float(newPrice))*100
    
    dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={idPortfolio} and (id_security={idSecuritie} or id_security=36) order by id_securitie')
    totalQuantity = dataBase.fetchall()
    
    dataBase.execute(f'select sec_date, quotation from quotations_history where id_securitie={idSecuritie}')
    history = dataBase.fetchall()
    
    graphLine = {
        'days': [],
        'count': [],
        'sum': 1
    }
    
    history = history[-7: ]
    
    for item in history: 
        graphLine['days'].append(item[0])
        graphLine['count'].append(item[1])
    
    data = {
      'security_name': security[0],
      'security_price': security[1],
      'graph_line': graphLine,
      'proc': proc,
      'total_quantity': fti(security[1]),
      'total_quantity': totalQuantity[0],
      'balance': totalQuantity[1]
    }
  
    connection.close()
    return data