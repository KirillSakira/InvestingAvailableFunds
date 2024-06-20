from django.shortcuts import render
from django.http import HttpResponseRedirect

from .viewBack.getUserData import getUserData
from .viewBack.getColorImg import getColorImg

from app.scripts.analytics.short.shortAnalyticsBalance import shortAnalyticsBalance
from app.scripts.analytics.short.shortAnalyticsBar import shortAnalyticsBar
from app.scripts.analytics.short.shortAnalyticsPie import shortAnalyticsPie
from app.scripts.analytics.all.getAnalyticsPie import analyticsPie

from app.scripts.clientProfile import private_profile
from app.scripts.OperationsWithBalance.operationsHistory import history
from app.scripts.mainPages.enterprise.enterpriseMainPage import enterpriseMainPage

#manager
from app.scripts.mainPages.manager.managerMainPage import managerMainPage

def chAuth(request):
    if request.session.session_key == None:
        return HttpResponseRedirect("/auth/")
    return None

def ret(request, url, data):
    chAuth(request)
    return render(request, url, data)
    
def toOops():
        return HttpResponseRedirect("/oops/")

def viewOops(request):
        return render(request, 'oops.html')

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
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)

    if userData['role'] == 'enterprise':
        aBal, aProc = shortAnalyticsBalance(request)
        aBarMonth, aBarCount, aBarSum = shortAnalyticsBar(request)
        aPie = shortAnalyticsPie(request)
        balanceData, secData, entName = enterpriseMainPage(request)
        data = {
            'userData': userData,
            'in_scripts_graph': True,
            
            'balance': balanceData['balance'],
            'var_balance': balanceData['var_balance'],
            'var_balance_proc': balanceData['balance_proc'],
            'var_balance_1': aBal,
            'var_balance_proc_1': aProc,
            'graph_bar': {
                'month': aBarMonth,
                'count': aBarCount,
                'sum': aBarSum
            },
            'graph_pie': aPie,
            'stocks_data': secData['stocks_data'],
            'bonds_data': secData['bonds_data'],
            'funds_data': secData['funds_data'],
            'curr_metals_data': secData['curr_metals_data']
        }
        return ret(request, 'index.html', data)
    elif userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'users': managerMainPage(request)
        }
        return ret(request, 'Mindex.html', data)
    else:
        return ret(request, '/auth.html')



def viewProfile(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    data = private_profile(request)
    return ret(request, 'profile.html', data)


def viewPayment(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    data = {
        'userData': getUserData(request)
    }
    return ret(request, 'payment.html', data)
    

def viewWithdraw(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    data = {
        'userData': getUserData(request)
    }
    return ret(request, 'withdraw.html', data)


def viewOperations(request):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    data = history(request)[1]
    if userData['role'] == 'enterprise':
        data = {
            'userData': userData,
            'operations_data': data
        }
        return ret(request, 'operations.html', data)
    elif userData['role'] == 'Manager':
        data = {
            'userData': userData,
            'bodyClass': 'operations_list',
            'operations_data': data
        }
        return ret(request, 'operations.html', data)
    else:
        return ret(request, '/auth.html')
    
def viewOperationsDetail(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    name, data = history(request, id)
    if userData['role'] == 'Manager':
        if data == 'Error':
            return toOops()
        
        data = {
            'userData': userData,
            'name': name,
            'operations_data': data
        }
        return ret(request, 'MoperationsDetail.html', data)
    else:
        return ret(request, '/auth.html')


def viewAnalytic(request, id=None):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)
    datas = analyticsPie(request)
    
    if datas != 'Error':
        for key in datas[0].keys():
            icos = getColorImg([obj['img'] for obj in datas[1][key]])
            for obj, col in zip(datas[0][key], icos):
                obj['color'] = col

    data = {
        'userData': userData,
        'in_scripts_graph': True,
        'in_slick': True,
        
        'pie': datas[0],
        'securities': datas[1],
    }
    return ret(request, 'analytic.html', data)
    



#Manager
def viewEnterprise(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
    userData = getUserData(request)

    if userData['role'] == 'Manager':
        aBal, aProc = shortAnalyticsBalance(request, id)
        aBarMonth, aBarCount, aBarSum = shortAnalyticsBar(request, id)
        aPie = shortAnalyticsPie(request, id)
        balanceData, secData, entName = enterpriseMainPage(request, id)

        if 'Error' in [aBal, aPie, aBarMonth, balanceData]:
            return toOops()

        data = {
            'userData': userData,
            'id': id,
            'in_scripts_graph': True,
                        
            'enterprise_name': entName,
            'balance': balanceData['balance'],
            'var_balance': balanceData['var_balance'],
            'var_balance_proc': balanceData['balance_proc'],
            'var_balance_1': aBal,
            'var_balance_proc_1': aProc,
            'graph_bar': {
                'month': aBarMonth,
                'count': aBarCount,
                'sum': aBarSum
            },
            'graph_pie': aPie,
            'stocks_data': secData['stocks_data'],
            'bonds_data': secData['bonds_data'],
            'funds_data': secData['funds_data'],
            'curr_metals_data': secData['curr_metals_data']
        }
        return ret(request, 'index.html', data)
    else:
        return ret(request, '/auth.html')

def viewTradeHistory(request, id):
    if chAuth(request) != None:
        return chAuth(request)
    
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


def viewTrade(request):
    if chAuth(request) != None:
        return chAuth(request)
    
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
