from connection import connection_db
from app.scripts.funcs import *

def getUserData(request):
	# connection = connection_db()
	# dataBase = connection.cursor()
	# name = request.user.last_name + request.user.first_name
	# dataBase.execute(f'select id_user, patronimic from auth_user where id={request.user.id}')
	# data = dataBase.fetchall()[0]
	# name += data[1]
	# dataBase.execute(f'select id_employee, id_enterprise from users where id_user={data[0]}')
	# data = dataBase.fetchall()[0]
	# if (data[0] == None):
	# 	dataBase.close()
	# 	connection.close()
	# 	return returnJson({
	# 		'name': name,
	# 		'role': 'enterprise'
	# 	})
	# else:
	# 	dataBase.execute(f'select id_post from employees where id_employee={data[1]}')
	# 	data = dataBase.fetchall()[0][0]
	# 	dataBase.execute(f'select post_name from posts where id_post={data}')
	# 	role = dataBase.fetchall()[0][0]
	# 	if role == 'Администратор':
	# 		role = 'Admin'
	# 	else:
	# 		role = 'Manager'
	# 	dataBase.close()
	# 	connection.close()
	# 	return returnJson({
	# 		'name': name,
	# 		'role': role
	# 	})
    return {
			'name': 'Иванов Иван Иванович',
			'role': 'user'
	}