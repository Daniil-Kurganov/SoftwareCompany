from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WindowAuthorization(object):
    def setupUi(self, WindowAuthorization):
        WindowAuthorization.setObjectName("WindowAuthorization")
        WindowAuthorization.resize(206, 202)
        self.centralwidget = QtWidgets.QWidget(WindowAuthorization)
        self.centralwidget.setObjectName("centralwidget")
        self.PushButtonAuthorization = QtWidgets.QPushButton(self.centralwidget)
        self.PushButtonAuthorization.setGeometry(QtCore.QRect(60, 150, 75, 23))
        self.PushButtonAuthorization.setObjectName("PushButtonAuthorization")
        self.TextEditLoginInput = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEditLoginInput.setGeometry(QtCore.QRect(20, 50, 161, 31))
        self.TextEditLoginInput.setObjectName("TextEditLoginInput")
        self.TextEditPasswordInput = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEditPasswordInput.setGeometry(QtCore.QRect(20, 100, 161, 31))
        self.TextEditPasswordInput.setObjectName("TextEditPasswordInput")
        self.LabelTitle = QtWidgets.QLabel(self.centralwidget)
        self.LabelTitle.setGeometry(QtCore.QRect(60, 20, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LabelTitle.setFont(font)
        self.LabelTitle.setObjectName("LabelTitle")
        WindowAuthorization.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(WindowAuthorization)
        self.statusbar.setObjectName("statusbar")
        WindowAuthorization.setStatusBar(self.statusbar)

        self.retranslateUi(WindowAuthorization)
        QtCore.QMetaObject.connectSlotsByName(WindowAuthorization)

    def retranslateUi(self, WindowAuthorization):
        _translate = QtCore.QCoreApplication.translate
        WindowAuthorization.setWindowTitle(_translate("WindowAuthorization", "SC: Auhorization window"))
        self.PushButtonAuthorization.setText(_translate("WindowAuthorization", "Войти"))
        self.LabelTitle.setText(_translate("WindowAuthorization", "Авторизация"))
