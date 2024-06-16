from connection import connection_db

def history(request):
    id = request.user.id

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f'select id_user from auth_user where id={id}')
    id_user = dataBase.fetchall()[0][0]
    dataBase.execute(f'select id_enterprise from Users where id_user={id_user}')
    id_enterprise = dataBase.fetchall()[0][0]
    dataBase.execute(f'select id_portfolio from Portfolios where id_enterprise={id_enterprise}')
    id_portfolio = dataBase.fetchall()[0][0]
    dataBase.execute(f'select * from Operations_History where id_portfolio={id_portfolio}')
    operations = dataBase.fetchall()

    data = []

    if operations == None:
        dataBase.close()
        connection.close()
        return data
    for operation in operations:
        operationType = operation[2]
        operationStatus = operation[3]
        operationDate = operation[4]
        operationAmount = operation[5]

        if(operationStatus):
            operationTypes = ['Вывод', 'Пополнение']
            operationData = {
                'type': operationTypes[int(operationType)],
                'date': operationDate,
                'price': operationAmount,
                'proc': ''
            }
            data.append(operationData)
    dataBase.close()
    connection.close()
    return data






