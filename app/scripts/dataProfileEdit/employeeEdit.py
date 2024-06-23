from connection import *
from app.scripts.funcs import *


def employeeEdit(request):
    user_id = request.POST.get('id')
    email = request.POST.get('email')
    name = request.POST.get('name')

    errorsDict = {}

    if len(email) > 150:
        errorsDict['email'] = 'Почта слишком длинная'

    if check(email, 'mail'):
        errorsDict['email'] = 'Введите корректную почту'

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict['name'] = 'ФИО введён некорректно'
    else:

        last_name, first_name, *args = splitName

        last_name = last_name.capitalize()
        first_name = first_name.capitalize()
        patronymic = ''

        if args != []:
            patronymic = args[0].capitalize()

        if len(first_name) > 150 or len(last_name) > 150 or len(patronymic) > 150:
            errorsDict['name'] = 'ФИО слишком длинное'

    if errorsDict != {}:
        return returnJson(data=errorsDict)

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"update auth_user set email='{email}' where id={user_id}")

    dataBase.execute(f"update auth_user set first_name='{splitName[0]}' set last_name='{splitName[1]}' set patronymic='{splitName[2]} where id={user_id}'")
    
    
    connection.commit()
    dataBase.close()
    connection.close()
    return returnJson(status='success', message='Данные обновлены')