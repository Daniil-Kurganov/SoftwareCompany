import psycopg2

try:
    connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
    with connection.cursor() as cursor:
        string_request = "INSERT INTO {}({}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s);".format('accounts', 'id', 'login', 'passwd',
                                                                                                  'privilege', 'idowner')
        cursor.execute(string_request, (5, ))
        print('{}'.format(cursor.fetchall()))
except Exception as error: print('Возникла ошикбка по подключению к БД:\n', error)
finally:
    if connection: connection.close()



# with connection.cursor() as cursor:
#     string_request = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog') AND table_schema IN('public', 'myschema');"
#     cursor.execute(string_request)
#     list_sql_result = cursor.fetchall()
# for tuple_current_table_name in list_sql_result:
#     list_dbtables.append(DBTable(tuple_current_table_name[0]))