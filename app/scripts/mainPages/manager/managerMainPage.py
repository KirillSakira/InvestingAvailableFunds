from connection import connection_db
from managerMainPage import *


def managerMainPage(request):
    fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)
    id = request.user.id

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from auth_user where id={id}')
    user_id = dataBase.fetchall()[0][0]
    
    data = []

    dataBase.execute(f'select id_employee from Users where id_user={user_id}')
    idEmployee = dataBase.fetchall()[0][0]

    dataBase.execute(f'select * from Portfolios where id_employee={idEmployee}')
    portfolios = dataBase.fetchall()

    if portfolios == None:
        dataBase.close()
        connection.close()
        return data
    for portfolio in portfolios:
        portfolioInfo = getPortfolioData(portfolio)
        data.append(portfolioInfo)

    dataBase.close()
    connection.close()
    return data







