import sys
import psycopg2
from PyQt5.QtWidgets import QMessageBox
from WindowAuthorization import *

class DBTable:
    def __init__(self, string_name):
        self.string_name = string_name
        self.list_columns_names = []
        with connection.cursor() as cursor:
            string_sql_reqest = 'SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;'
            cursor.execute(string_sql_reqest, (self.string_name,))
            list_authorization_result = cursor.fetchall()
        for tuple_current_column_name in list_authorization_result:
            self.list_columns_names.append(tuple_current_column_name[0])
        print(self.list_columns_names)
def authorization() -> None:
    '''Процесс авторизации'''
    global sting_password, string_privilege
    with connection.cursor() as cursor:
        string_sql_request = "SELECT * FROM accounts WHERE login = %s AND passwd = %s"
        cursor.execute(string_sql_request, (str(ui.TextEditLoginInput.toPlainText()), str(ui.TextEditPasswordInput.toPlainText())))
        tuple_authorization_result = cursor.fetchone()
        if tuple_authorization_result != None: sting_password, string_privilege = tuple_authorization_result[2], tuple_authorization_result[3]
        else: show_error_message(13, 'Пользователь с такими данными не существует.')
        return None
def show_error_message(int_error_key: int, string_error_massage: str) -> None:
    '''Вывод ошибок'''
    dictionary_error_texts = {6: 'Ошибка подключения к БД', 13: 'Ошибка авторизации'}
    message_error = QMessageBox()
    message_error.setIcon(QMessageBox.Critical)
    message_error.setText(dictionary_error_texts[int_error_key])
    message_error.setInformativeText(string_error_massage)
    message_error.setWindowTitle("Ошибка!")
    message_error.exec_()
    return None

app = QtWidgets.QApplication(sys.argv)
WindowAuthorization = QtWidgets.QMainWindow()
ui = Ui_WindowAuthorization()
ui.setupUi(WindowAuthorization)
WindowAuthorization.show()
try:
    connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
    dbtable_employees = DBTable("employees")
    dbtable_accounts = DBTable('accounts')
    dbtable_customers = DBTable("customers")
    dbtable_projects = DBTable('projects')
    dbtable_technicaltasks = DBTable('technicaltasks')
    dbtable_projectteams = DBTable('projectteams')
    dbtable_agreements= DBTable('agreements')
    dbtable_services = DBTable('services')
    ui.PushButtonAuthorization.clicked.connect(authorization)
except Exception as string_error: show_error_message(6, string_error)
sys.exit(app.exec_())
if connection: connection.close()