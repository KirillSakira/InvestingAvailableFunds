from django.shortcuts import render
from django.http import HttpResponseRedirect

from .viewBack.getUserData import getUserData
from .viewBack.getColorImg import getColorImg

from app.scripts.clientProfile import private_profile
from app.scripts.OperationsWithBalance.operationsHistory import history

def ret(request, url, data):
    if request.session.session_key != None:
        return render(request, url, data)
    else:
        return HttpResponseRedirect("/auth/")


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


def viewHome(request):
    userData = getUserData(request)
    if userData['role'] == 'enterprise':
        data = {
            'userData': userData,
            'in_scripts_graph': True,
            
            'balance': '18 638 725,7',
            'balance_proc': '+19,45',
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
        return ret(request, 'index.html', data)
    elif userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'users': [
                {
                    'id': '1',
                    'name': 'Паровозов А. Д.',
                    'balance': '18 638 725,7',
                    'balance_proc': '+19,45',
                },
                {
                    'id': '2',
                    'name': 'Паssровозов А. Д.',
                    'balance': '1 625,7',
                    'balance_proc': '-9,45',
                }
            ]
        }
        return ret(request, 'Mindex.html', data)



def viewProfile(request):
    # data = {
    #     'userData': getUserData(request),
    #     'email': 'asdas@asdasd.asd',
    #     'gender': 'Мужской',
    #     'name': 'asdasd asdasdasda sdasdasds',
    #     'phone': '+79192837475',
    #     'sn_passport': '03 03 030303',
    #     'address': 'ewwwwwwwwwwwwwwwww wwwwwwwwwwwwwwwwwwwwww wwwwwwwwww23ew',
    #     'birday': '01.01.1010'
    # }
    data = private_profile(request)
    return ret(request, 'profile.html', data)


def viewPayment(request):
    data = {
        'userData': getUserData(request)
    }
    return ret(request, 'payment.html', data)
    

def viewWithdraw(request):
    data = {
        'userData': getUserData(request)
    }
    return ret(request, 'withdraw.html', data)


def viewOperations(request):
    userData = getUserData(request)
    if userData['role'] == 'enterprise':
        data = {
            'userData': userData,
            'operations_data': history(request)
        }
        return ret(request, 'operations.html', data)
    elif userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'bodyClass': 'operations_list',
            'operations_data': [
                {
                    'id': '1',
                    'type': 'Пополнение',
                    'date': '01.01.2021 15:30',
                    'name': 'Паровозов А. Д.',
                    'price': '+7 895',
                    'proc': '+3'
                },
                {
                    'id': '2',
                    'type': 'Снятие',
                    'date': '01.10.2021 15:30',
                    'name': 'Карапузиков И. В.',
                    'price': '-5 895',
                    'proc': '-2'
                },
                {
                    'id': '3',
                    'type': 'Пополнение',
                    'date': '01.01.2023 15:30',
                    'name': 'Валялько Д. К.',
                    'price': '+1 895',
                    'proc': '+1'
                }
            ]
        }
        return ret(request, 'operations.html', data)
    
def viewOperationsDetail(request, id):
    userData = getUserData(request)

    #по url получаем id пользователя и выдаем инфу

    if userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'name': 'Паровозов А. Д.',
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
                }
            ]
        }
        return ret(request, 'MoperationsDetail.html', data)


def viewAnalytic(request, id=None):
    userData = getUserData(request)
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
                'count': '250',
                'proc': '25',
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
                'count': '250',
                'proc': '25',
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
                'count': '200',
                'proc': '20',
                'img': 'b1.png',
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
                'img': 'b2.png',
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
                'count': '250',
                'proc': '25',
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
                'count': '250',
                'proc': '25',
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
                'count': '200',
                'proc': '20',
                'img': 's2.png',
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
                'count': '250',
                'proc': '25',
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
                'count': '250',
                'proc': '25',
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
                'count': '200',
                'proc': '20',
                'img': 's2.png',
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
                'count': '250',
                'proc': '25',
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
                'count': '250',
                'proc': '25',
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
                'count': '200',
                'proc': '20',
                'img': 's2.png',
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
        'userData': userData,
        'in_scripts_graph': True,
        'in_slick': True,
        
        'stocs': stocks_data,
        'bonds': bonds_data,
        'funds': funds_data,
        'curr_metals': curr_metals_data
    }
    return ret(request, 'analytic.html', data)
    



#Manager
def viewEnterprise(request, id):
    userData = getUserData(request)

    if userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'id': id,
            'in_scripts_graph': True,
            
            'enterprise_name': 'Аркадий Паровозов',
            'balance': '18 638 725,7',
            'balance_proc': '+19,45',
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
                    'proc_end': '+50'
                }
            ]
        }
        return ret(request, 'index.html', data)
    else:
        return ret(request, '/auth.html')

def viewTradeHistory(request, id):
    userData = getUserData(request)

    if userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'id': id,
            'sec_data': [
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
            ]
        }
        return ret(request, 'tradeHistory.html', data)
    else:
        return ret(request, '/auth.html')


def viewTrade(request, id):
    userData = getUserData(request)

    if userData['role'] == 'Manager':
        data = {
            'userData': userData,
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
            'funds_data': [
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
            'curr_metals_data': [
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
            ]
        }
        return ret(request, 'trade.html', data)
    else:
        return ret(request, '/auth.html')
