import psycopg2

try:
    connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
    with connection.cursor() as cursor:
        string_request = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog') AND table_schema IN('public', 'myschema');"
        cursor.execute(string_request)
        # cursor.execute("SELECT * FROM accounts WHERE login = 'dk3012';")
        print('{}'.format(cursor.fetchall()))
except Exception as error: print('Возникла ошикбка по подключению к БД:\n', error)
finally:
    if connection: connection.close()