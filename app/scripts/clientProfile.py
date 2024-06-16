from connection import connection_db

def private_profile(request):
    id = request.user.id

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"select * from auth_user where id={id}")
    data = dataBase.fetchall()[0]
    lastName = data[6]
    firstName = data[5]
    patronymic = data[12]
    email = data[7]
    id_user = data[11]

    dataBase.execute(f"select id_enterprise from Users where id_user={id_user}")
    id_enterprise = dataBase.fetchall()[0][0]

    dataBase.execute(f"select * from Enterprises where id_enterprise={id_enterprise}")
    data = dataBase.fetchall()[0]
    phone = data[4]
    address = data[3]
    
    if patronymic == None:
        patronymic = ''

    data = {
        'email': email,
        'name': (lastName + ' ' + firstName + ' ' + patronymic).strip(),
        'phone': phone,
        'address': address
    }

    dataBase.close()
    connection.close()
    return data