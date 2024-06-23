from connection import *
from app.scripts.funcs import *


def clientEdit(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    phone = request.POST.get('phone').replace('+7', '8')
    address = request.POST.get('address')
    idUser = request.POST.get('id')

    errorsDict = {}

    if len(email) > 150:
        errorsDict['email'] = 'Почта слишком длинная'

    if len(address) > 150:
        errorsDict['address'] = 'Адрес слишком длинный'

    if check(email, 'mail'):
        errorsDict['email'] = 'Введите корректную почту'

    if not (len(phone) == 11 and phone.isdigit()):
        errorsDict['phone'] = 'Телефон введён некорректно'

    splitName = name.split()

    if len(splitName) < 2:
        errorsDict['name'] = 'ФИО введён некорректно'
    else:

        lastName, firstName, *args = splitName

        lastName = lastName.capitalize()
        firstName = firstName.capitalize()
        patronymic = ''

        if args != []:
            patronymic = args[0].capitalize()

        if len(firstName) > 150 or len(lastName) > 150 or len(patronymic) > 150:
            errorsDict['name'] = 'ФИО слишком длинное'

    if errorsDict != {}:
        return returnJson(data=errorsDict)

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"update auth_user set email='{email}' where id={idUser}")
    
    dataBase.execute(f"update auth_user set first_name='{splitName[0]}' set last_name='{splitName[1]}' set patronymic='{splitName[2]} where id={idUser}'")
    
    dataBase.execute(f'select id_user from auth_user where id={idUser}')
    idUser = dataBase.fetchall()[0][0]
    
    dataBase.execute(f"update enterprises update set tel='{phone}' where id_user={idUser}")
    
    dataBase.execute(f"update enterprises update set address='{address}' where id_user={idUser}")
    
    connection.commit()
    dataBase.close()
    connection.close()
    return returnJson(status='success', message='Данные обновлены')