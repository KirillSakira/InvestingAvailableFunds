from connection import connection_db
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .regModule import *

def registrationDjango(request):
	
	role = request.POST.get('role')
	username = request.POST.get('login')
	password = request.POST.get('password')
	name = request.POST.get('name')
	email = request.POST.get('email')
	phone = request.POST.get('phone')
	address = request.POST.get('address')
	title = request.POST.get('title')
	typeProperty = request.POST.get('typeProperty')
	
	if username == None:
		username = email
	
	errorsDict = {}
	returnErrors = False
	
	idEmployee = 'Null'
	idEnterprise = 'Null'
	
	if len(email) > 150:
		errorsDict['email'] = 'Почта слишком длинная'
	
	if len(address) > 150:
		errorsDict['address'] = 'Адрес слишком длинный'
	
	if len(title) > 100:
		errorsDict['title'] = 'Название организации слишком длинное'
	
	if len(typeProperty) > 50:
		errorsDict['typeProperty'] = 'Тип собственности слишком длинный'
	
	if len(password) < 8:
		errorsDict['password'] = 'Пароль слишком короткий'
	
	if checkPass(password):
		errorsDict['password'] = 'Пароль имеет недопустимые символы'
	
	if User.objects.filter(username=username).exists():
		errorsDict['email'] = 'Пользователь уже существует'
		
	if check(email, 'mail'):
		errorsDict['email'] = 'Введите корректную почту'
	
	splitName = name.split()
	
	if len(splitName) < 2:
		errorsDict['name'] = 'ФИО введён некорректно'
	else:
	
		last_name, first_name, *args = splitName
		
		patronimic = 'Null'
		
		if args != []:
			patronimic = args[0]
		
	
		if len(first_name) > 150 or len(last_name) > 150 or len(patronimic) > 150:
			errorsDict['name'] = 'ФИО слишком длинное'
	
	returnErrors = errorsDict == {}
	
	connection = connection_db()
	dataBase = connection.cursor()
	
	if not role in ['Admin', 'Manager']:
		
		phone = phone.replace('+7', '8')
		
		if not (len(phone) == 11 and phone.isdigit()):
			errorsDict['phone'] = 'Телефон введён некорректно'
		
		dataBase.execute(f'select tel from enterprises where tel=\'{phone}\'')
		result = dataBase.fetchall()
		if result != []:
			errorsDict['phone'] = 'Телефон уже используется'
		
		if address.replace(' ', '') == '':
			errorsDict['address'] = 'Введите адрес'
			
		if title.replace(' ', '') == '':
			errorsDict['title'] = 'Введите название компании'
		
		if typeProperty.replace(' ', '') == '':
			errorsDict['typeProperty'] = 'Введите тип собственности'
		
		returnErrors = errorsDict != {}
		
		if not returnErrors:
			dataBase.execute(insertsql('enterprises', [title, typeProperty, address, phone]))
			
			idEnterprise = getId(dataBase, 'enterprises', 'id_ent')
	else:
		if role == 'Admin':
			dataBase.execute('insert into employees values (default, 1)')
		
		elif role == 'Manager':
			dataBase.execute('insert into employees values (default, 2)')
		
		idEmployee = getId(dataBase, 'employees', 'id_employee')
	
	if returnErrors:
		dataBase.close()
		connection.close()
		return returnJson(data=errorsDict)

	dataBase.execute(f'insert into users values (default, {idEmployee}, {idEnterprise})')
	
	idUser = getId(dataBase, 'users', 'id_user')
	
	user = User.objects.create_user(
		username=username,
		password=password,
		first_name=first_name,
		last_name=last_name,
		email=email
	)
	
	user.save()
	
	user = authenticate(request, username=username, password=password)
	login(request, user)
	
	dataBase.execute(f'update auth_user set id_user={idUser} where username=\'{username}\'')
	
	dataBase.execute(f'update auth_user set patronimic=\'{patronimic}\' where username=\'{username}\'')
	
	connection.commit()
	dataBase.close()
	connection.close()
	return returnJson(status='success')