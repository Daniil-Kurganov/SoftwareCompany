import sys
import psycopg2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from GUI_PY.WindowAuthorization import *
from GUI_PY.WindowWorkWithDBTables import *

class DBTable:
    def __init__(self, string_name) -> None:
        self.string_name = string_name
        self.list_columns_names, self.list_columns_data_types = [], []
        self.dictionary_query = {'insert': 'INSERT INTO {}('.format(self.string_name),
                                 'update': 'UPDATE {} SET ('.format(self.string_name),
                                 'delete': 'DELETE FROM {} WHERE id = %s;'.format(self.string_name)}
        connection = get_db_connection()
        with connection.cursor() as cursor:
            string_sql_reqest = 'SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;'
            cursor.execute(string_sql_reqest, (self.string_name,))
            list_authorization_result = cursor.fetchall()
        connection.close()
        string_query = ''
        for tuple_current_column in list_authorization_result:
            self.list_columns_names.append(str(tuple_current_column[0]))
            string_query += tuple_current_column[0] + ', '
            if tuple_current_column[1] == 'bigint': self.list_columns_data_types.append(int)
            else: self.list_columns_data_types.append(str)
        string_insert_query = string_query[:-2] + ') VALUES (' + ('%s, ' * len(self.list_columns_names))
        string_update_query = string_query[:-2] + ') = (' + ('%s, ' * len(self.list_columns_names))
        self.dictionary_query['insert'] += string_insert_query[:-2] + ');'
        self.dictionary_query['update'] += string_update_query[:-2] + ') WHERE id = %s;'
        print(self.dictionary_query['update'])
        return None
def authorization() -> None:
    '''Процесс авторизации'''
    global sting_password, string_privilege
    connection = get_db_connection()
    with connection.cursor() as cursor:
        string_sql_request = "SELECT * FROM accounts WHERE login = %s AND passwd = %s"
        cursor.execute(string_sql_request, (str(ui.TextEditLoginInput.toPlainText()), str(ui.TextEditPasswordInput.toPlainText())))
        tuple_authorization_result = cursor.fetchone()
        if tuple_authorization_result != None:
            ui.TextEditLoginInput.clear()
            ui.TextEditPasswordInput.clear()
            sting_password, string_privilege = tuple_authorization_result[2], tuple_authorization_result[3]
            WorkWithDBTables()
        else: show_error_message(13, 'Пользователь с такими данными не существует.')
    connection.close()
    return None
def show_error_message(int_error_key: int, string_error_massage: str) -> None:
    '''Вывод ошибок'''
    dictionary_error_texts = {6: 'Ошибка подключения к БД', 13: 'Ошибка авторизации', 451: 'Ошибка работы с БД'}
    message_error = QMessageBox()
    message_error.setIcon(QMessageBox.Critical)
    message_error.setText(dictionary_error_texts[int_error_key])
    message_error.setInformativeText(string_error_massage)
    message_error.setWindowTitle("Ошибка!")
    message_error.exec_()
    return None
def WorkWithDBTables() -> None:
    '''Функция окна работы с табоицами БД'''
    global WindowWorkWithDBTables

    def show_dbtable() -> None:
        '''Вывод данных таблицы БД'''
        int_current_dbtables_index = ui.ComboBoxCurrentDBTable.currentIndex()
        connection = get_db_connection()
        with connection.cursor() as cursor:
            string_request = "SELECT * FROM {};".format(list_dbtables[int_current_dbtables_index].string_name)
            cursor.execute(string_request)
            list_current_dbtable_data = cursor.fetchall()
        connection.close()
        ui.TableWidgetDBTableData.setRowCount(len(list_current_dbtable_data))
        ui.TableWidgetDBTableData.setColumnCount(len(list_current_dbtable_data[0]))
        ui.TableWidgetDBTableData.verticalHeader().setVisible(False)
        ui.TableWidgetDBTableData.setHorizontalHeaderLabels(list_dbtables[int_current_dbtables_index].list_columns_names)
        for int_current_row_index in range(len(list_current_dbtable_data)):
            for int_current_column_index in range(len(list_current_dbtable_data[int_current_row_index])):
                ui.TableWidgetDBTableData.setItem(int_current_row_index, int_current_column_index, QTableWidgetItem(
                                                        str(list_current_dbtable_data[int_current_row_index][int_current_column_index])))
        ui.ComboBoxIdMutableNote.clear()
        for tuple_current_note in list_current_dbtable_data:
            ui.ComboBoxIdMutableNote.addItem(str(tuple_current_note[0]))
        return None
    def logout() -> None:
        '''Выход из учётной записи'''
        WindowWorkWithDBTables.hide()
        WindowAuthorization.show()
        return None
    def set_admin_state() -> None:
        '''Установка настроек окна для аккаунта admin'''
        ui.RadioButtonInsertNote.setEnabled(True)
        ui.RadioButtonEditNote.setEnabled(True)
        ui.RadioButtonDeleteNote.setEnabled(True)
        ui.ComboBoxIdMutableNote.setEnabled(True)
        return None
    def insert_mode_activate() -> None:
        '''Вектор внеснения новой записи в таблицу БД'''
        ui.TextEditWorkspace.setEnabled(True)
        ui.PushButtonDoExtion.setEnabled(True)
        ui.PushButtonInsertSeparator.setEnabled(True)
        ui.TextEditWorkspace.clear()
        return None
    def edit_or_delete_mode_activate() -> None:
        '''Вектор изменения текущих записей в таблице БД'''
        ui.TextEditWorkspace.setEnabled(True)
        ui.PushButtonDoExtion.setEnabled(True)
        ui.ComboBoxIdMutableNote.setEnabled(True)
        ui.PushButtonInsertSeparator.setEnabled(True)
        connection = get_db_connection()
        with connection.cursor() as cursor:
            string_sql_request = "SELECT * FROM {} WHERE id = %s;".format(list_dbtables[ui.ComboBoxCurrentDBTable.currentIndex()].string_name)
            cursor.execute(string_sql_request, (str(ui.ComboBoxIdMutableNote.currentText()),))
            tuple_sql_request_result = cursor.fetchone()
        connection.close()
        ui.TextEditWorkspace.setText('$_%_$'.join(str(item_current) for item_current in tuple_sql_request_result))
        return None
    def do_extion_with_dbtable() -> None:
        '''Выполнить выбранную операцию с таблицей БД'''
        try:
            dbtable = list_dbtables[ui.ComboBoxCurrentDBTable.currentIndex()]
            list_current_data = ui.TextEditWorkspace.toPlainText().split('$_%_$')
            int_current_iteration = 0
            for type_current_data in dbtable.list_columns_data_types:
                list_current_data[int_current_iteration] = type_current_data(list_current_data[int_current_iteration])
                int_current_iteration += 1
            connection = get_db_connection()
            if ui.RadioButtonInsertNote.isChecked():
                with connection.cursor() as cursor: cursor.execute(dbtable.dictionary_query['insert'], list_current_data)
            elif ui.RadioButtonDeleteNote.isChecked():
                with connection.cursor() as cursor: cursor.execute(dbtable.dictionary_query['delete'], (int(ui.ComboBoxIdMutableNote.currentText()),))
            elif ui.RadioButtonEditNote.isChecked():
                list_current_data.append(list_current_data[0])
                with connection.cursor() as cursor:
                    cursor.execute(dbtable.dictionary_query['update'], list_current_data)
            connection.commit()
            connection.close()
            ui.TextEditWorkspace.clear()
        except Exception as string_error: show_error_message(451, str(string_error))
        return None
    def insert_separator_to_workspace() -> None:
        '''Подстановка сепаратора в рабочую облать'''
        cursor =  ui.TextEditWorkspace.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText('$_%_$')
        ui.TextEditWorkspace.setTextCursor(cursor)
        return None

    WindowWorkWithDBTables = QtWidgets.QMainWindow()
    ui = Ui_WindowWorkWithDBTables()
    ui.setupUi(WindowWorkWithDBTables)
    WindowAuthorization.close()
    WindowWorkWithDBTables.show()
    if string_privilege == 'Администратор': set_admin_state()
    elif string_privilege == 'Привилегированный пользователь': ui.RadioButtonInsertNote.setEnabled(True)
    ui.ComboBoxCurrentDBTable.currentIndexChanged.connect(show_dbtable)
    ui.PushButtonLogOut.clicked.connect(logout)
    ui.RadioButtonInsertNote.clicked.connect(insert_mode_activate)
    ui.RadioButtonEditNote.clicked.connect(edit_or_delete_mode_activate)
    ui.RadioButtonDeleteNote.clicked.connect(edit_or_delete_mode_activate)
    ui.PushButtonInsertSeparator.clicked.connect(insert_separator_to_workspace)
    ui.PushButtonDoExtion.clicked.connect(do_extion_with_dbtable)
    return None
def get_db_connection() -> psycopg2:
    '''Подключение к БД'''
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='123456789', dbname='SoftwareCompanyDB', port=5432)
        return connection
    except Exception as string_error:
        show_error_message(6, string_error)
        exit(666)

app = QtWidgets.QApplication(sys.argv)
WindowAuthorization = QtWidgets.QMainWindow()
ui = Ui_WindowAuthorization()
ui.setupUi(WindowAuthorization)
WindowAuthorization.show()
list_dbtables = []
list_dbtables.append(DBTable('projects'))
list_dbtables.append(DBTable('agreements'))
list_dbtables.append(DBTable('technicaltasks'))
list_dbtables.append(DBTable('customers'))
list_dbtables.append(DBTable('services'))
list_dbtables.append(DBTable('employees'))
list_dbtables.append(DBTable('projectteams'))
list_dbtables.append(DBTable('accounts'))
ui.PushButtonAuthorization.clicked.connect(authorization)
sys.exit(app.exec_())