from django.shortcuts import render
from django.http import HttpResponseRedirect

from .viewBack.getProfileName import getProfileName

def viewAuth(request):
    if request.session.session_key == None:
        return render(request, 'auth.html')
    else:
        return HttpResponseRedirect("/")

def viewRegistration(request):
    if request.session.session_key == None:
        return render(request, 'registration.html')
    else:
        return HttpResponseRedirect("/")

def viewProfile(request):
    data = {
        'email': 'asdas@asdasd.asd',
        'gender': 'Мужской',
        'name': 'asdasd asdasdasda sdasdasds',
        'phone': '+79192837475',
        'sn_passport': '03 03 030303',
        'address': 'ewwwwwwwwwwwwwwwww wwwwwwwwwwwwwwwwwwwwww wwwwwwwwww23ew',
        'birday': '01.01.1010'
    }
    if request.session.session_key != None:
        return render(request, 'profile.html', data)
    else:
        return render(request, 'profile.html', data)
        # return HttpResponseRedirect("/auth/")

def viewHome(request):
    data = {
        'profileName': getProfileName(),
        'balance': '18 638 725,7',
        'var_balance': '8 736 976.33',
        'var_balance_proc': '+19,45',
        'var_balance_1': '18 638 725,7',
        'var_balance_proc_1': '+19,56',
        'pie_stock': '30',
        'pie_bonds': '25',
        'pie_funds': '25',
        'pie_curr_metals': '20',
        'graph_pie': [100, 200, 300, 300],
        'graph_bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'stocks_data': [
            {
                'img': 's1.png', #имя
                'name': 'Норильский никель', #имя
                'short_name': 'GMKN', #сокращенное имя
                'price_buy': '15 975 876,66', #цена покупки
                'price_now': '16 200 000,31', #текущая цена
                'price_count_buy': '15 975 876,66', #цена всех купленных
                'count_buy': '10', #количество купленных
                'price_end': '+1 975 876,66', #сколько пользователь получил/потерял
                'proc_end': '+3' #в процентах
            },
            {
                'img': 's2.png',
                'name': 'ТКС Холдинг',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            },
            {
                'img': 's3.png',
                'name': 'Яндекс',
                'short_name': 'YNDX',
                'price_buy': '4 155,96',
                'price_now': '4 161,4',
                'price_count_buy': '12 448,2',
                'count_buy': '3',
                'price_end': '+8 544,78',
                'proc_end': '+17,92'
            },
            {
                'img': 's2.png',
                'name': 'ТКС Холдинг',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            },
            {
                'img': 's3.png',
                'name': 'Яндекс',
                'short_name': 'YNDX',
                'price_buy': '4 155,96',
                'price_now': '4 161,4',
                'price_count_buy': '12 448,2',
                'count_buy': '3',
                'price_end': '+8 544,78',
                'proc_end': '+17,92'
            }
        ],
        'bonds_data': [
            {
                'name': 'Норильский никель',
                'short_name': 'GMKN',
                'price_buy': '15 975 876,66',
                'count_buy': '10',
                'price_now': '16 200 000,31',
                'price_end': '+1 975 876,66',
                'proc_end': '+3'
            },
            {
                'name': 'ААААААААААААААА',
                'short_name': 'аааааа',
                'price_buy': '77777',
                'count_buy': '100',
                'price_now': '999999',
                'price_end': '+236524',
                'proc_end': '+50    '
            }
        ],
        'funds_data': [
            {
                'name': 'Норильский никель',
                'short_name': 'GMKN',
                'price_buy': '15 975 876,66',
                'count_buy': '10',
                'price_now': '16 200 000,31',
                'price_end': '+1 975 876,66',
                'proc_end': '+3'
            },
            {
                'name': 'ААААААААААААААА',
                'short_name': 'аааааа',
                'price_buy': '77777',
                'count_buy': '100',
                'price_now': '999999',
                'price_end': '+236524',
                'proc_end': '+50    '
            }
        ],
        'curr_metals_data': [
            {
                'name': 'Норильский никель',
                'short_name': 'GMKN',
                'price_buy': '15 975 876,66',
                'count_buy': '10',
                'price_now': '16 200 000,31',
                'price_end': '+1 975 876,66',
                'proc_end': '+3'
            },
            {
                'name': 'ААААААААААААААА',
                'short_name': 'аааааа',
                'price_buy': '77777',
                'count_buy': '100',
                'price_now': '999999',
                'price_end': '+236524',
                'proc_end': '+50    '
            }
        ]
    }
    if request.session.session_key != None:
        return render(request, 'index.html', data)
    else:
        return render(request, 'index.html', data)
        # return HttpResponseRedirect("/auth/")