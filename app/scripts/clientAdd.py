from connection import connection_db
from app.scripts.funcs import returnJson

def clientAdd(request):
	connection = connection_db()
	dataBase = connection.cursor()
	
	idE = request.user.id
	username = request.POST.get('email')
	
	dataBase.execute(f'select id_user from auth_user where username=\'{username}\'')
	idUserEnt = dataBase.fetchall()
	if idUserEnt == []:
		return returnJson(status='error', message='Такого пользователя не существует')
	idUserEnt = idUserEnt[0][0]
	dataBase.execute(f'select id_enterprise from users where id_user={idUserEnt}')
	idEnterprise = dataBase.fetchall()[0][0]
	if idEnterprise == None:
		return returnJson(status='error', message='Такого клиента не существует')
	dataBase.execute(f'select id_employee from portfolios where id_enterprise={idEnterprise}')
	if dataBase.fetchall()[0][0] != None:
		return returnJson(status='error', message='Клиент уже работает с другим менеджером')
	
	
	dataBase.execute(f'select id_user from auth_user where id={idE}')
	idUserEmp = dataBase.fetchall()[0][0]
	dataBase.execute(f'select id_employee from users where id_user={idUserEmp}')
	idEmployee = dataBase.fetchall()[0][0]
	
	# dataBase.execute(f'update portfolios set id_employee={idEmployee} where id_enterprise={idEnterprise}')
	
	connection.commit()
	dataBase.close()
	connection.close()
	return returnJson(status='success')