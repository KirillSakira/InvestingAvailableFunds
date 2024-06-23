from connection import *


def adminMainPage(request):
    connection = connection_db()
    dataBase = connection.cursor()
    
    cursor.execute('select id_user, first_name, last_name, patronymic from auth_user')
    data = dataBase.fetchall()
    
    dataBase.execute('select id_user from users u where id_enterprise=Nsull and (select id_post from employees where id_employee=u.id_employee)=2')
    idEmployees = dataBase.fetchall()
    
    dataBase.execute('select id_user from users where id_employee=Null')
    idClients = dataBase.fetchall()
    
    dataBase.close()
    connection.close()
    
    employees = []
    employees += (temp for temp in data if temp[0] in [temp2[0] for temp2 in idEmployees])
    
    clients = []
    clients += (temp for temp in data if temp[0] in [temp2[0] for temp2 in idClients])
    
    clientsData = []
    employeesData = []
    
    for temp in clients:
        clientsData.append({
            'id': temp[0],
            'fio': f"{temp[1]} {temp[2]} {temp[3]}".strip()
        })
    
    for temp in employees:
        employeesData.append({
            'id': temp[0],
            'fio': f"{temp[1]} {temp[2]} {temp[3]}".strip()
        })
    data = {
        'clients': clientsData,
        'employees': employeesData
    }
    return data