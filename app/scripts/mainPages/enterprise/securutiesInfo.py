from connection import connection_db


def securutiesInfo(securities):
    connection = connection_db()
    dataBase = connection.cursor()

    info = []

    for securitie in securities:
        idSecuritie = securitie[1]
        totalQuantity = securitie[2]

        dataBase.execute(f'select id_catalog, sec_name, ticker, quotation, icon from securities where id_securitie={idSecuritie}')
        idCatalog, securitieName, ticker, currentQuotation, iconPath = dataBase.fetchall()[0]

        currentTotalPrice = currentQuotation * totalQuantity

        dataBase.execute(f'select quantity, total_price from requests where id_securitie={idSecuritie}')
        data = dataBase.fetchall()[0]
        oldQuantity = data[0]
        oldTotalPrice = data[1]
        oldQuotation = oldTotalPrice / oldQuantity
        securitieInfo = {
            'Каталог актива': idCatalog,
            'name': securitieName,
            'short_name': ticker,
            'Путь к иконке': iconPath,
            'price_buy': oldQuotation,
            'price_now': currentQuotation,
            'price_count_buy': currentTotalPrice,
            'count_buy': totalQuantity,
            'price_end': (oldQuotation - currentQuotation) * totalQuantity,
            'proc_end': (oldQuotation - currentQuotation) / (oldQuotation * 0.01)
        }
        info.append(securitieInfo)

    return info