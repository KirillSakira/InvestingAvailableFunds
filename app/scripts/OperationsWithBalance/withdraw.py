from babloss.app.scripts.authorisation.regModule import returnJson
import psycopg2
from django.contrib.sessions.models import Session
from django.utils.dateparse import parse_date
from datetime import datetime
from connection import connection_db

def withdrawBack(request):
    amount = int(request.POST.get('amount'))
    card_number = request.POST.get('card_number')
    card_date = request.POST.get('card_date')
    card_date = parse_date(card_date)

    errors_dict = {}

    if amount <= 0:
        errors_dict['amount'] = 'Некорректная сумма перевода'

    if len(card_number) != 16:
        errors_dict['card_number'] = 'Некорректный номер карты'

    if card_date.year < datetime.today().year:
        errors_dict['card_date'] = 'Карта недействительна или некорректный срок действия карты'

    if request.user.is_authenticated == False:
        errors_dict['authenticated'] = 'Необходимо авторизоваться.'

    checker = errors_dict != {}

    if checker:
        return returnJson(data=errors_dict)

    user_id = request.user.id
    
    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(f"select id_enterprise from Users where user_id='{user_id}'")
    id_enterprise = cursor.fetchall()[0][0]

    cursor.execute(f"select id_portfolio from Portfolios where id_enterprise='{id_enterprise}'")
    id_portfolio = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO Operations_History (id_portfolio, oper_type, amount) VALUES('{id_portfolio}', '{False}', '{amount}');")
    connection.commit()

    cursor.execute("select oper_status from Operations_History where id_oper = (select max(id_oper) from Operations_History)")
    oper_status = cursor.fetchall()[0][0]



    if oper_status == False:
        errors_dict['amount'] = 'Недостаточно свободных средств'
        return returnJson(data=errors_dict['amount'])


    cursor.execute(f"select id_employee from Portfolios where id_enterprise='{id_enterprise}'")
    id_employee = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO Messages (id_sender, id_receiver, message_date, message_content) VALUES('{user_id}', '{id_employee}', 'default', 'Было совершено снятие клиентом № {user_id}');")
    connection.commit()
    cursor.close()
    connection.close()

    return returnJson(status='Success', message='Успешное снятие')