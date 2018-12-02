# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(340, 260)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 300, 211))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 211, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_pass = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_pass.setObjectName("lbl_pass")
        self.gridLayout.addWidget(self.lbl_pass, 1, 0, 1, 1)
        self.tb_user = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.tb_user.setObjectName("tb_user")
        self.gridLayout.addWidget(self.tb_user, 0, 1, 1, 1)
        self.tb_pass = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.tb_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tb_pass.setClearButtonEnabled(False)
        self.tb_pass.setObjectName("tb_pass")
        self.gridLayout.addWidget(self.tb_pass, 1, 1, 1, 1)
        self.lbl_user = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_user.setObjectName("lbl_user")
        self.gridLayout.addWidget(self.lbl_user, 0, 0, 1, 1)
        self.btn_login = QtWidgets.QPushButton(self.groupBox)
        self.btn_login.setGeometry(QtCore.QRect(100, 140, 60, 30))
        self.btn_login.setObjectName("btn_login")
        self.btn_cancel = QtWidgets.QPushButton(self.groupBox)
        self.btn_cancel.setGeometry(QtCore.QRect(180, 140, 60, 30))
        self.btn_cancel.setObjectName("btn_cancel")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(LoginWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.groupBox.setTitle(_translate("LoginWindow", "登入"))
        self.lbl_pass.setText(_translate("LoginWindow", "密碼："))
        self.lbl_user.setText(_translate("LoginWindow", "帳號："))
        self.btn_login.setText(_translate("LoginWindow", "登入"))
        self.btn_cancel.setText(_translate("LoginWindow", "取消"))
        self.actionExit.setText(_translate("LoginWindow", "Exit"))
        self.actionExit.setShortcut(_translate("LoginWindow", "Esc"))

