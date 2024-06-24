from connection import connection_db


def getSecuritiesByCatalog(request, userId):
    fti = lambda f: float(str(round(f, 2))) if f != int(f) else int(f)
    
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_user from auth_user where id={userId}')
    idUser = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
       on p.id_enterprise = u.id_enterprise where u.id_user = {idUser}''')
    idPortfolio = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'''select s.sec_name, s.ticker, s.quotation, COALESCE(ps.total_quantity, 0) total_quantity, s.id_catalog, s.id_securitie
                     from securities s 
                     left join (select * from portfolio_to_securitie 
                        where id_portfolio = {idPortfolio}) ps 
                        on s.id_securitie = ps.id_securitie 
                     order by s.id_securitie''')
    result = dataBase.fetchall()
    data = {
        'stocks_data': [],
        'bonds_data': [],
        'funds_data': [],
        'curr_metals_data': []
    }
    
    template = list(data.keys())
    template.insert(0, '')
    
    for i in result:
        d = {
            'name': i[0],
            'short_name': i[1],
            'price_now': fti(i[2]),
            'count_buy': fti(i[3]),
            'id': i[4],
            'price_portfolio': i[2]*i[3],
            'id_sec': i[5]
        }
        dataBase.execute(f"select quotation from quotations_history where id_securitie={d['id_sec']}")
        try:
            d['old_price'] = fti(dataBase.fetchall()[-2][0])
            d['proc'] = fti(d['price_portfolio']/(d['count_buy'] * d['old_price']) * 100)
        except:
            d['old_price'] = 0
            d['proc'] = 0
        if d['id_sec'] != 36:
            data[template[d['id']]].append(d)
    
    dataBase.close()
    connection.close()
    return data