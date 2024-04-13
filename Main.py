import sys
from WindowAuthorization import *

def authorization() -> None:
    '''Процесс авторизации'''
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM services')
        print('{}'.format(cursor.fetchall()))
def show_error_message(int_error_key, string_error_massage: str) -> None:
    '''Вывод ошибок'''
    dictionary_error_texts = {6: 'Ошибка подключения к БД'}
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
try: connection = psycopg2.connect(host = 'localhost', user = 'postgres', password = '123456789', dbname = 'SoftwareCompanyDB', port = 5432)
except Exception as string_error: show_error_message(string_error)
finally:
    if connection: connection.close()
sys.exit(app.exec_())