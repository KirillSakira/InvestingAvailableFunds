from app.scripts.funcs import returnJson
from connection import connection_db

def withdrawBack(request):
    amount = int(request.POST.get('amount'))
    card_number = request.POST.get('card_number')

    errors_dict = {}

    if amount <= 0:
        errors_dict['amount'] = 'Некорректная сумма перевода'

    if len(card_number) != 16:
        errors_dict['card_number'] = 'Некорректный номер карты'

    checker = errors_dict != {}

    if checker:
        return returnJson(data=errors_dict)

    user_id = request.user.id
    
    connection = connection_db()
    cursor = connection.cursor()
    
    cursor.execute(f'select id_user from auth_user where id={user_id}')
    id_user = cursor.fetchall()[0][0]

    cursor.execute(f"select id_enterprise from users where id_user='{id_user}'")
    id_enterprise = cursor.fetchall()[0][0]

    cursor.execute(f"select id_portfolio from portfolios where id_enterprise='{id_enterprise}'")
    id_portfolio = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO operations_history (id_portfolio, oper_type, amount) VALUES('{id_portfolio}', '{False}', '{amount}');")
    connection.commit()

    cursor.execute("select oper_status from operations_history where id_operation = (select max(id_operation) from operations_history)")
    oper_status = cursor.fetchall()[0][0]



    if oper_status == False:
        errors_dict['message'] = 'Недостаточно свободных средств'
        return returnJson(data=errors_dict)


    cursor.execute(f"select id_employee from Portfolios where id_enterprise='{id_enterprise}'")
    id_employee = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO Messages (id_sender, id_receiver, message_date, message_content) VALUES('{user_id}', '{id_employee}', 'default', 'Было совершено снятие клиентом № {user_id}');")
    connection.commit()
    cursor.close()
    connection.close()

    return returnJson(status='success', message='Успешное снятие')