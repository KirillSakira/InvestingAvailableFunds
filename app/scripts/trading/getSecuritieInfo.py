from connection import connection_db
from app.scripts.funcs import fti, numFormat
from app.scripts.trading.getPromotionsNew import get_graph_info


def getSecuritieInfo(request, userId, ticker): 
    type = {
      1: {
        'eng': 'stocks',
        'rus': 'акций',
        'href_rus': 'акции'
      },
      2: {
        'eng': 'bonds',
        'rus': 'облигаций',
        'href_rus': 'облигации'
      },
      3: {
        'eng': 'funds',
        'rus': 'фондов',
        'href_rus': 'фонды'
      },
      4: {
        'eng': 'curr_metals',
        'rus': 'ценных металлов',
        'href_rus': 'ценные металлы'
      }
    }
    
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_securitie from securities where ticker=\'{ticker}\'')
    idSecuritie = dataBase.fetchall()[0][0]

    dataBase.execute(f'select id_user from auth_user where id={userId}')
    idUser = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={idUser}')
    idPortfolio = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'select sec_name, quotation, icon, id_catalog from securities where id_securitie={idSecuritie}')
    security = dataBase.fetchall()[0]
    
    dataBase.execute(f'select quotation from queue where id_securitie={idSecuritie} and id_portfolio={idPortfolio} order by queue_date')
    try:
      oldPrice = dataBase.fetchall()[0][0]
      
      newPrice = security[1]
      proc = 100 - (float(oldPrice)/float(newPrice))*100
    except:
      proc = 0
    
    dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={idPortfolio} and (id_securitie={idSecuritie} or id_securitie=36) order by id_securitie')
    totalQuantity = dataBase.fetchall()
    
    
    if len(totalQuantity) == 2:
      balance = totalQuantity[1][0]
      totalQuantity = totalQuantity[0][0]
    else:
      balance = totalQuantity[0][0]
      totalQuantity = 0
    
    graphLine = get_graph_info(ticker, type[security[3]]['href_rus'])

    data = {
      'security_name': security[0],
      'security_price': fti(float(graphLine["1 day"][-1]["price"]) if len(graphLine["1 day"]) else 0),
      'security_img': security[2],
      'graph_line': graphLine,
      'proc': fti(proc),
      'total_sum': fti(fti(security[1]) * fti(totalQuantity)),
      'total_quantity1': numFormat(fti(totalQuantity)),
      'balance': numFormat(fti(balance)),
      'type': type[security[3]]
    }
  
    connection.close()
    return data