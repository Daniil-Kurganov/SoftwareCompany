import psycopg2

try:
    connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
    with connection.cursor() as cursor:
        string_request = "SELECT * FROM accounts WHERE login = %s"
        cursor.execute(string_request, ('dk3012',))
        # cursor.execute("SELECT * FROM accounts WHERE login = 'dk3012';")
        print('{}'.format(cursor.fetchone()[0]))
except Exception as error: print('Возникла ошикбка по подключению к БД:\n', error)
finally:
    if connection: connection.close()