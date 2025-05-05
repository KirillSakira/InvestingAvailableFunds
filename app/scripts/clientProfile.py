from connection import connection_db

def private_profile(request, id=None):
    try:
        id = id if id != None else request.user.id

        connection = connection_db()
        dataBase = connection.cursor()

        dataBase.execute(f"select first_name, last_name, email, id_user, patronymic from auth_user where id={id}")
        firstName, lastName, email, id_user, patronymic = dataBase.fetchall()[0]

        dataBase.execute(f"select id_enterprise from Users where id_user={id_user}")
        id_enterprise = dataBase.fetchall()[0][0]

        dataBase.execute(f"select title, type_property, tel, address from Enterprises where id_enterprise={id_enterprise}")
        data = dataBase.fetchall()[0]
        title, typeProperty, phone, address = data
        
        if patronymic == None:
            patronymic = ''

        data = {
            'email': email,
            'name': (lastName + ' ' + firstName + ' ' + patronymic).strip(),
            'phone': phone,
            'address': address,
            'type_property': typeProperty,
            'title': title
        }

        dataBase.close()
        connection.close()
        return data
    except:
        return 'Error'