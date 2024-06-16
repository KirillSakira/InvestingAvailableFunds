from connection import connection_db
from securutiesInfo import *


def enterpriseMainPage(request):
    id = request.user.id

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from auth_user where id={id}')
    data = dataBase.fetchall()[0]
    id_user = data[0]

    dataBase.execute(f'select id_enterprise from users where id_user={id_user}')
    data = dataBase.fetchall()[0]
    id_enterprise = data[0]

    dataBase.execute(f'select * from portfolios where id_enterprise={id_enterprise}')
    data = dataBase.fetchall()[0]
    balance = data[3]
    deposition = data[4]
    id_portfolio = data[0]
    balanceChange = balance - deposition
    balanceChangePercentage = balanceChange / (deposition * 0.01)

    balanceInfo = {
        'balance': balance,
        'var_balance': balanceChange,
        'balance_proc': balanceChangePercentage
    }

    data = []
    data.append(balanceInfo)

    dataBase.execute(f'select * from portfolios_to_securitie where id_portfolio={id_portfolio}')
    securities = dataBase.fetchall()

    if securities == None:
        dataBase.close()
        connection.close()
        return data

    data.append(securutiesInfo(securities))
    dataBase.close()
    connection.close()
    return data
