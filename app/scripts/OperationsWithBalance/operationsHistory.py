from connection import connection_db

def history(request):
    id = request.user.id

    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(f"select id_user from auth_user where id='{id}'")
    id_user = cursor.fetchall()[0][0]
    cursor.execute(f"select id_enterprise from Users where id_user='{id_user}'")
    id_enterprise = cursor.fetchall()[0][0]
    cursor.execute(f"select id_portfolio from Portfolios where id_enterprise='{id_enterprise}'")
    id_portfolio = cursor.fetchall()[0][0]
    cursor.execute(f"select * from Operations_History where id_portfolio='{id_portfolio}'")
    operations = cursor.fetchall()

    data = []

    if operations == None:
        cursor.close()
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
                'Тип операции': operationTypes[int(operationType)],
                'Дата и время операции': operationDate,
                'Сумма операции': operationAmount
            }
            data.append(operationData)
    cursor.close()
    connection.close()
    return data






