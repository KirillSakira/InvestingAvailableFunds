from connection import connection_db


def getSecuritiesByCatalog(request, userId):
    connection = connection_db()
    dataBase = connection.cursor()
    
    dataBase.execute(f'select id_user from auth_user where id={userId}')
    idUser = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'''select id_portfolio from portfolios as p join users as u
       on p.id_enterprise = u.id_enterprise where u.id_user = {idUser}''')
    idPortfolio = dataBase.fetchall()[0][0]
    
    dataBase.execute(f'''select s.sec_name, s.ticker, s.quotation, COALESCE(ps.total_quantity, 0) total_quantity, s.id_catalog 
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
            'price_now':i[2],
            'count_buy':i[3],
            'id':i[4]
        }
        if d['id'] != 36:
            data[template[d['id']]].append(d)
    
    dataBase.close()
    connection.close()
    return data