import psycopg2

try:
    connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
    with connection.cursor() as cursor:
        string_request = "UPDATE accounts SET ({}, {}, {}, {}, {}) = (%s, %s, %s, %s, %s) WHERE id = %s;".format('id', 'login',
                                                                                                                   'passwd', 'privilege', 'idowner')
        cursor.execute(string_request, [7, 'lof', 'f,d', 'Пользователь', 2, 7])
        # # print('{}'.format(cursor.fetchall()))
        # string_sql_reqest = 'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;'
        # cursor.execute(string_sql_reqest, ('accounts',))
        # list_authorization_result = cursor.fetchall()
        # print(list_authorization_result)
except Exception as error: print('Возникла ошикбка по подключению к БД:\n', error)
finally:
    if connection: connection.close()



# with connection.cursor() as cursor:
#     string_request = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog') AND table_schema IN('public', 'myschema');"
#     cursor.execute(string_request)
#     list_sql_result = cursor.fetchall()
# for tuple_current_table_name in list_sql_result:
#     list_dbtables.append(DBTable(tuple_current_table_name[0]))