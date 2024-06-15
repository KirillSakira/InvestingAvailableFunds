from connection import connection_db

def private_profile(request):
    id = request.user.id

    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(f"select * from auth_user where id='{id}'")
    data = cursor.fetchall()
    last_name = data[0][6]
    first_name = data[0][5]
    patronymic = data[0][12]
    email = data[0][7]
    id_user = data[0][11]

    cursor.execute(f"select id_enterprise from Users where id_user='{id_user}'")
    id_enterprise = cursor.fetchall()[0][0]

    cursor.execute(f"select * from Enterprises where id_enterprise='{id_enterprise}'")
    data = cursor.fetchall()
    phone = data[0][4]
    address = data[0][3]

    data = {
        'email': email,
        'name': (last_name + ' ' + first_name + ' ' + patronymic).strip(),
        'phone': phone,
        'address': address
    }

    cursor.close()
    connection.close()
    return data




















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
            if(operationType):
                operationData = {
                    'Тип операции': 'Пополнение',
                    'Дата и время операции': operationDate,
                    'Сумма операции': operationAmount
                }
                data.append(operationData)
            else:
                operationData = {
                'Тип операции' : 'Снятие',
                'Дата и время операции' : operationDate,
                'Сумма операции' : operationAmount
                }
                data.append(operationData)
    cursor.close()
    connection.close()
    return data





