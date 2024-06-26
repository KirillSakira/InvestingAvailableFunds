from connection import *


def adminMainPage():
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute('select id_user, first_name, last_name, patronymic from auth_user')
    data = dataBase.fetchall()
    
    dataBase.execute('select id_user from users u where id_enterprise is Null and (select id_post from employees where id_employee=u.id_employee)=2')
    idEmployees = dataBase.fetchall()
    
    dataBase.execute('select id_user from users where id_employee is Null')
    idClients = dataBase.fetchall()
    
    employees = []
    employees += (temp for temp in data if temp[0] in [temp2[0] for temp2 in idEmployees])
    
    clients = []
    clients += (temp for temp in data if temp[0] in [temp2[0] for temp2 in idClients])
    
    clientsData = []
    employeesData = []
    
    for temp in clients:
        dataBase.execute(f'select id from auth_user where id_user={temp[0]}')
        id = dataBase.fetchall()[0][0]
        if temp[3] == None:
            temp[3] = ''
        clientsData.append({
            'id': id,
            'fio': f"{temp[1]} {temp[2][0]}. {temp[3][0]}.".strip()
        })
    
    for temp in employees:
        dataBase.execute(f'select id from auth_user where id_user={temp[0]}')
        id = dataBase.fetchall()[0][0]
        if temp[3] == None:
            temp[3] = ''
        employeesData.append({
            'id': id,
            'fio': f"{temp[1]} {temp[2][0]}. {temp[3][0]}.".strip()
        })
    data = {
        'clients': clientsData,
        'employees': employeesData
    }
    dataBase.close()
    connection.close()
    return data