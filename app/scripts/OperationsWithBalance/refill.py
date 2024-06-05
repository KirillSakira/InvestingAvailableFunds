from connection import connection_db
from app.scripts.funcs import returnJson
import psycopg2
from django.contrib.sessions.models import Session
from django.utils.dateparse import parse_date
from datetime import datetime

def refillBack(request):

    amount = int(request.POST.get('amount'))
    card_number = request.POST.get('card_number')
    card_date = request.POST.get('card_date')
    card_date = parse_date(card_date)

    if amount <= 0:
        return returnJson(status='Error', message='Некорректная сумма перевода')

    if len(card_number) != 16:
        return returnJson(status='Error', message='Некорректный номер карты')

    if card_date is None:
        return returnJson(status='Error', message='Некорректная срок действия карты')

    if card_date.year < datetime.today().year:
        return returnJson(status='Error', message='Карта недействительна или некорректный срок действия карты')

    if request.user == None:
        return returnJson(status='Error', message='Необходимо авторизоваться.')

    user_id = request.user.id

    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(f"select id_enterprise from Users where user_id='{user_id}'")
    id_enterprise = cursor.fetchall()[0][0]

    cursor.execute(f"select id_portfolio from Portfolios where id_enterprise='{id_enterprise}'")
    id_portfolio = cursor.fetchall()[0][0]
    
    cursor.execute(f"INSERT INTO Operations History (id_portfolio, oper_type, amount) VALUES('{id_portfolio}', '{True}', '{amount}');")
    connection.commit()

    cursor.execute(f"select id_employee from Portfolios where id_enterprise='{id_enterprise}'")
    id_employee = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO Messages (id_sender, id_receiver, message_date, message_content) VALUES('{user_id}', '{id_employee}', 'default', 'Было совершено пополнение клиентом №{user_id} в размере {amount}₽');")
    connection.commit()
    cursor.close()
    connection.close()

    return returnJson(status='Success', message='Успешное пополнение')
