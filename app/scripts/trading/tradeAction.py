from connection import connection_db
from app.scripts.funcs import returnJson


def tradeAction(request):
    id_securitie = request.POST.get('id_securitie')
    action = bool(request.POST.get('action'))
    quantity = request.POST.get('quantity')
    userId = request.POST.get('uid')

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from auth_user where id={userId}')
    id_user = dataBase.fetchall()[0][0]
    dataBase.execute(
        f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={id_user}')
    id_portfolio = dataBase.fetchall()[0][0]

    if action:
        dataBase.execute(
            f'insert into requests (id_portfolio, id_securitie, quantity, req_type) values ({id_portfolio}, {id_securitie}, {quantity}, true)')

        connection.commit()

        dataBase.execute(f'select req_status from requests where id_request = (select max(id_request) from requests)')
        oper_status = dataBase.fetchall()[0][0]

        if not (oper_status):
            dataBase.close()
            connection.close()
            return returnJson(status='error', message='Недостаточно свободных средств')

        dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={id_portfolio} and (id_securitie={id_securitie} or id_securitie=36) order by id_securitie')
        newTotalQuantity = dataBase.fetchall()[0][0]
        newBalance = dataBase.fetchall()[1][0]
        dataBase.close()
        connection.close()
        return returnJson(data={
            'total_quantity': newTotalQuantity,
            'balance': newBalance,
            'status': 'success',
            'message': 'Покупка совершена успешно'
        })

    dataBase.execute(f'insert into requests (id_portfolio, id_securitie, quantity, req_type) values ({id_portfolio}, {id_securitie}, {quantity}, false)')
    connection.commit()
    dataBase.execute(f'select req_status from requests where id_request = (select max(id_request) from requests)')
    oper_status = dataBase.fetchall()[0][0]

    if not (oper_status):
        dataBase.close()
        connection.close()
        return returnJson(status='error', message='Указано неверное колличество для продажи')

    dataBase.execute(
        f'select total_quantity from portfolio_to_securitie where id_portfolio={id_portfolio} and (id_securitie={id_securitie} or id_securitie=36) order by id_securitie')
    newTotalQuantity = dataBase.fetchall()[0][0]
    newBalance = dataBase.fetchall()[1][0]
    dataBase.close()
    connection.close()
    return returnJson(data={
        'total_quantity': newTotalQuantity,
        'balance': newBalance,
        'status': 'success',
        'message': 'Продажа совершена успешно'
    })