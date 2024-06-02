import psycopg2
def connection_db():
    return psycopg2.connect("dbname=test5 user=postgres password=1234 host=localhost port=5432")