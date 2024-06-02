from django.http import HttpResponse
from re import findall
from json import dumps

def check(string, param):
	patterns = {
		'mail': r'\b[\w\d]+@\w+\.\w+\b'
	}
	return findall(patterns[param], string) == []

def insertsql(table, params):
	return f'''insert into {table}
values
(default, \'''' + '\', \''.join(params) + '\')'

def getId(cursor, table, idColumn):
	cursor.execute(f'select {idColumn} from {table}')
	result = cursor.fetchall()
	return result[-1][0]

def checkPass(password):
	availableSymbols = [i for i in range(48, 58)]
	availableSymbols.extend([i for i in range(97, 123)])
	return list(filter(lambda g: not(ord(g) in availableSymbols), list(password.lower()))) != []

def returnJson(data={}, status='', message=''):
	if data == {}:
		data2 = {
			'status': status,
			'message': message
		}
	else:
		data2 = data
	return HttpResponse(dumps(data2, ensure_ascii=False), content_type='application/json')
