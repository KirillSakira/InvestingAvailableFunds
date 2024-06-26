from connection import connection_db
from app.scripts.funcs import returnJson

def delete_profile(request):
    id = request.user.id

    connection = connection_db()
    dataBase = connection.cursor()

    dataBase.execute(f"select id_user from auth_user where id={id}")
    idUser = dataBase.fetchall()[0][0]

    dataBase.execute(f"select id_enterprise from users where id_user={idUser}")
    idEnterprise = dataBase.fetchall()[0][0]

    dataBase.execute(f"select * from portfolios where id_enterprise={idEnterprise}")
    idPortfolio = dataBase.fetchall()[0][0]
    
    dataBase.execute(f"delete from queue where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from portfolio_to_securitie where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from operations_history where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from balances_history where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from requests where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from portfolios where id_portfolio={idPortfolio}")
    dataBase.execute(f"delete from users where id_enterprise={idEnterprise}")
    dataBase.execute(f"delete from auth_user where id={id}")
    dataBase.execute(f"delete from enterprises where id_enterprise={idEnterprise}")

    connection.commit()
    dataBase.close()
    connection.close()
    return returnJson(status="success", message="Ваш аккаунт был удалён")