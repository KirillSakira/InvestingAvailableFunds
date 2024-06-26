from connection import connection_db
from app.scripts.funcs import *
import re

def getUserData(request):
	fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)
	connection = connection_db()
	dataBase = connection.cursor()
	name = request.user.last_name + ' ' + request.user.first_name
	dataBase.execute(f'select id_user, patronymic from auth_user where id={request.user.id}')
	data = dataBase.fetchall()[0]
	if data[1] != None:
		name += ' ' + data[1]
	dataBase.execute(f'select id_employee, id_enterprise from users where id_user={data[0]}')
	data = dataBase.fetchall()[0]
	if (data[0] == None):
		userId = request.user.id
    
		dataBase.execute(f'select id_user from auth_user where id={userId}')
		idUser = dataBase.fetchall()[0][0]
		
		dataBase.execute(f'select id_portfolio from portfolios as p join users as u on p.id_enterprise=u.id_enterprise where u.id_user={idUser}')
		idPortfolio = dataBase.fetchall()[0][0]
		
		dataBase.execute(f'select total_quantity from portfolio_to_securitie where id_portfolio={idPortfolio} and id_securitie=36')
		totalQuantity = dataBase.fetchall()[0][0]
		
		dataBase.close()
		connection.close()
		return {
			'name': name,
			'role': 'enterprise',
			'balance': f"{fti(totalQuantity):,.0f}".replace(',', ' ')
		}
	else:
		dataBase.execute(f'select id_post from employees where id_employee={data[0]}')
		data = dataBase.fetchall()[0][0]
		dataBase.execute(f'select post_name from posts where id_post={data}')
		role = dataBase.fetchall()[0][0]
		if role == 'Администратор':
			role = 'Admin'
		else:
			role = 'Manager'
		dataBase.close()
		connection.close()
		return {
			'name': name,
			'role': 'Admin'
		}
    
	
	
	
	# return {
	# 	'name': 'Иванов Иван Иванович',
	# 	'role': 'enterprise'
	# }