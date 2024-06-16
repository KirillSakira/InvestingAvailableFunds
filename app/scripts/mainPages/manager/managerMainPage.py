from connection import connection_db

def getInitials(id_enterprise):
    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from Users where id_enterprise={id_enterprise}')
    id_user = dataBase.fetchall()[0][0]

    dataBase.execute(f'select * from auth_user where id_user={id_user}')
    data = dataBase.fetchall()[0]
    clientLastName = data[6]
    clientFirstName = data[5]
    clientPatronymic = data[12]

    initials = f'{clientLastName} {clientFirstName[0]}.'
    if clientPatronymic != None:
        initials += f' {clientPatronymic[0]}.'
    return initials

def managerMainPage(request):
    id = request.user.id

    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(f'select * from auth_user where id={id}')
    data = cursor.fetchall()[0]
    employeeLastName = data[6]
    employeeFirstName = data[5]

    employeeInfo = {
        'Имя сотрудника': (f'{employeeFirstName} {employeeLastName}'),
    }

    data = []
    data.append(employeeInfo)

    cursor.execute(f'select id_employee from Users where id_user={id}')
    idEmployee = cursor.fetchall()[0][0]

    cursor.execute(f'select * from Portfolios where id_employee={idEmployee}')
    portfolios = cursor.fetchall()

    if portfolios == None:
        cursor.close()
        connection.close()
        return data
    for portfolio in portfolios:
        balance = portfolio[3]
        deposition = portfolio[4]
        initials = getInitials(portfolio[2])

        balanceChange = (balance - deposition) / (deposition * 0.01)
        portfolioInfo = {
            'Текущий баланс': balance,
            'Прирост/падение': balanceChange,
            '(клиент) Фамилия И. О.': initials
        }
        data.append(portfolioInfo)

    cursor.close()
    connection.close()
    return data







