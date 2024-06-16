from connection import connection_db


def shortAnalyticsPie(request):
    userId = request.user.id
    connection = connection_db()
    dataBase = connection.cursor()
    dataBase.execute(f'select id_user from auth_user where id={userId}')
    id_user = dataBase.fetchall()[0][0]
    dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
on p.id_enterprise = u.id_enterprise where u.id_user = {id_user}''')
    idPortfolio = dataBase.fetchall()[0][0]
    dataBase.execute(f'''select total_quantity, quotation, catalog_name
from portfolio_to_securitie as p join securities as s
on p.id_securitie = s.id_securitie join catalogs as c
on s.id_catalog = c.id_catalog where id_portfolio = {idPortfolio}''')
    data = dataBase.fetchall()
    dataBase.close()
    connection.close()
    quantities = {}
    totalSum = 0
    for row in data:
        idSecuritie = row[2]
        securitieQuantity = float(row[0] * row[1])
        totalSum += securitieQuantity
        quantities[idSecuritie] = securitieQuantity + quantities.get(idSecuritie, 0)
    graph_pie = []
    for key in quantities:
        graph_pie.append(
            {
                'name': key, 'proc': round(quantities[key] / totalSum * 100, 2),
                'count': round(quantities.get(key), 2)
            }
        )
    return graph_pie
