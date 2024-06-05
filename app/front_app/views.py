from django.shortcuts import render
from django.http import HttpResponseRedirect

from .viewBack.getProfileName import getProfileName
from .viewBack.getColorImg import getColorImg


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
        'profileName': getProfileName(),
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
        'in_scripts_graph': True,
        
        'profileName': getProfileName(),
        'balance': '18 638 725,7',
        'var_balance': '8 736 976.33',
        'var_balance_proc': '+19,45',
        'var_balance_1': '18 638 725,7',
        'var_balance_proc_1': '+19,56',
        'graph_bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'graph_pie': [
            {
                'name': 'Акции',
                'count': '100',
                'proc': '10',
                'color': '#3AA1FF'
            },
            {
                'name': 'Облигации',
                'count': '250',
                'proc': '25',
                'color': '#FF523A'
            },
            {
                'name': 'Фонды',
                'count': '250',
                'proc': '25',
                'color': '#F1EDFD'
            },
            {
                'name': 'Валюта и металлы',
                'count': '200',
                'proc': '20',
                'color': '#634FED'
            }
        ],
        'stocks_data': [
            {
                'img': 's1', #имя
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
                'img': 's2',
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
                'img': 's3',
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
                'img': 's2',
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
                'img': 's3',
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


def viewPayment(request):
    data = {
        'profileName': getProfileName()
    }
    if request.session.session_key != None:
        return render(request, 'payment.html', data)
    else:
        return render(request, 'payment.html', data)
        # return HttpResponseRedirect("/auth/")
    

def viewWithdraw(request):
    data = {
        'profileName': getProfileName()
    }
    if request.session.session_key != None:
        return render(request, 'withdraw.html', data)
    else:
        return render(request, 'withdraw.html', data)
        # return HttpResponseRedirect("/auth/")


def viewOperations(request):
    data = {
        'profileName': getProfileName(),
        'operations_data': [
            {
                'type': 'Пополнение',
                'date': '01.01.2021 15:30',
                'price': '+7 895',
                'proc': '+3'
            },
            {
                'type': 'Снятие',
                'date': '01.10.2021 15:30',
                'price': '-5 895',
                'proc': '-2'
            },
            {
                'type': 'Пополнение',
                'date': '01.01.2023 15:30',
                'price': '+1 895',
                'proc': '+1'
            },
        ]
    }
    if request.session.session_key != None:
        return render(request, 'operations.html', data)
    else:
        return render(request, 'operations.html', data)
        # return HttpResponseRedirect("/auth/")


def viewAnalytic(request):
    stocks_data = {
        'counts': {
            'count': '28 638 725,7',
            'proc': '+19,56'
        },
        'bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'pie': [
            {
                'count': '100',
                'proc': '10',
                'img': 's1', #имя
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
                'count': '250',
                'proc': '25',
                'img': 's2',
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
                'count': '250',
                'proc': '25',
                'img': 's3',
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
                'count': '200',
                'proc': '20',
                'img': 'b1',
                'name': 'руру1',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            },
            {
                'count': '200',
                'proc': '20',
                'img': 'b2',
                'name': 'руру2',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            }
        ]
    }
    stocks_data_icos = getColorImg([obj['img'] for obj in stocks_data['pie']])
    for obj, col in zip(stocks_data['pie'], stocks_data_icos):
        obj['color'] = col

    bonds_data = {
        'counts': {
            'count': '38 638 725,7',
            'proc': '+19,56'
        },
        'bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'pie': [
            {
                'count': '100',
                'proc': '10',
                'img': 's1', #имя
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
                'count': '250',
                'proc': '25',
                'img': 's2',
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
                'count': '250',
                'proc': '25',
                'img': 's3',
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
                'count': '200',
                'proc': '20',
                'img': 's2',
                'name': 'ТКС Холдинг',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            }
        ]
    }
    bonds_data_icos = getColorImg([obj['img'] for obj in bonds_data['pie']])
    for obj, col in zip(bonds_data['pie'], bonds_data_icos):
        obj['color'] = col

    funds_data = {
        'counts': {
            'count': '48 638 725,7',
            'proc': '+19,56'
        },
        'bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'pie': [
            {
                'count': '100',
                'proc': '10',
                'img': 's1', #имя
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
                'count': '250',
                'proc': '25',
                'img': 's2',
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
                'count': '250',
                'proc': '25',
                'img': 's3',
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
                'count': '200',
                'proc': '20',
                'img': 's2',
                'name': 'ТКС Холдинг',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            }
        ]
    }
    funds_data_icos = getColorImg([obj['img'] for obj in funds_data['pie']])
    for obj, col in zip(funds_data['pie'], funds_data_icos):
        obj['color'] = col

    curr_metals_data = {
        'counts': {
            'count': '58 638 725,7',
            'proc': '+19,56'
        },
        'bar': {
            'month': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            'count': [100, 400, 300, 324, 565, 233, 456, 111, 324, 234, 312, 234]
        },
        'pie': [
            {
                'count': '100',
                'proc': '10',
                'img': 's1', #имя
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
                'count': '250',
                'proc': '25',
                'img': 's2',
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
                'count': '250',
                'proc': '25',
                'img': 's3',
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
                'count': '200',
                'proc': '20',
                'img': 's2',
                'name': 'ТКС Холдинг',
                'short_name': 'TKSG',
                'price_buy': '2 798,45',
                'price_now': '1 598,89',
                'price_count_buy': '7 994,45',
                'count_buy': '5',
                'price_end': '-5 997,8',
                'proc_end': '-33,78'
            }
        ]
    }
    curr_metals_data_icos = getColorImg([obj['img'] for obj in curr_metals_data['pie']])
    for obj, col in zip(curr_metals_data['pie'], curr_metals_data_icos):
        obj['color'] = col

    data = {
        'profileName': getProfileName(),
        'in_scripts_graph': True,
        'in_slick': True,
        
        'stocs': stocks_data,
        'bonds': bonds_data,
        'funds': funds_data,
        'curr_metals': curr_metals_data
    }
    if request.session.session_key != None:
        return render(request, 'analytic.html', data)
    else:
        return render(request, 'analytic.html', data)
        # return HttpResponseRedirect("/auth/")