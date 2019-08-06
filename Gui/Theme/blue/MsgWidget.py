# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Msg(object):
    def setupUi(self, Msg):
        Msg.setObjectName("Msg")
        Msg.resize(450, 150)
        Msg.setStyleSheet("QWidget#widgetTitle {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(25, 50, 80, 255), stop:1 rgba(40, 45, 50, 255));\n"
"}\n"
"QWidget#widgetContent {\n"
"    \n"
"}\n"
"QWidget#widgetBottom {\n"
"    border-top-style: solid;\n"
"    border-top-width: 2px;\n"
"    border-top-color: rgba(60, 65, 70, 80);\n"
"}\n"
"\n"
"QLabel#lbl_title {\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QLabel#lbl_content {\n"
"    padding: 5px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton#btn_close {\n"
"    font-family: \"webdings\";\n"
"    color: rgb(160, 160, 160);\n"
"}\n"
"QPushButton#btn_close:hover {\n"
"    background-color: rgba(212, 64, 39, 0);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton#btn_minimized {\n"
"    font-family: \"webdings\";\n"
"    color: rgb(160, 160, 160);\n"
"}\n"
"QPushButton#btn_minimized:hover {\n"
"    background-color: rgba(212, 64, 39, 0);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton#btn_confirm {\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 1px;\n"
"    border: solid 3px rgb(255, 255, 255);\n"
"    font-weight: bold;\n"
"    \n"
"    background-color: rgb(70, 75, 80);\n"
"}\n"
"QPushButton#btn_confirm:hover {\n"
"    color: rgb(255, 255, 255);\n"
"    font-weight: bold;\n"
"    \n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Msg)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetTitle = QtWidgets.QWidget(Msg)
        self.widgetTitle.setMinimumSize(QtCore.QSize(0, 30))
        self.widgetTitle.setObjectName("widgetTitle")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetTitle)
        self.horizontalLayout_3.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_title = QtWidgets.QLabel(self.widgetTitle)
        self.lbl_title.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(8)
        self.lbl_title.setFont(font)
        self.lbl_title.setObjectName("lbl_title")
        self.horizontalLayout_3.addWidget(self.lbl_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_minimized = QtWidgets.QPushButton(self.widgetTitle)
        self.btn_minimized.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_minimized.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_minimized.setObjectName("btn_minimized")
        self.horizontalLayout_3.addWidget(self.btn_minimized)
        self.btn_close = QtWidgets.QPushButton(self.widgetTitle)
        self.btn_close.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_close.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_3.addWidget(self.btn_close)
        self.verticalLayout.addWidget(self.widgetTitle)
        self.widgetContent = QtWidgets.QWidget(Msg)
        self.widgetContent.setObjectName("widgetContent")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.widgetContent)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.lbl_icon = QtWidgets.QLabel(self.widgetContent)
        self.lbl_icon.setText("")
        self.lbl_icon.setObjectName("lbl_icon")
        self.hboxlayout.addWidget(self.lbl_icon)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.lbl_content = QtWidgets.QLabel(self.widgetContent)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        self.lbl_content.setFont(font)
        self.lbl_content.setWordWrap(True)
        self.lbl_content.setObjectName("lbl_content")
        self.hboxlayout.addWidget(self.lbl_content)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem3)
        self.hboxlayout.setStretch(0, 1)
        self.hboxlayout.setStretch(1, 15)
        self.hboxlayout.setStretch(2, 1)
        self.hboxlayout.setStretch(3, 60)
        self.hboxlayout.setStretch(4, 1)
        self.verticalLayout.addWidget(self.widgetContent)
        self.widgetBottom = QtWidgets.QWidget(Msg)
        self.widgetBottom.setObjectName("widgetBottom")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetBottom)
        self.horizontalLayout.setContentsMargins(0, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.btn_confirm = QtWidgets.QPushButton(self.widgetBottom)
        self.btn_confirm.setMinimumSize(QtCore.QSize(75, 25))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout.addWidget(self.btn_confirm)
        self.verticalLayout.addWidget(self.widgetBottom)
        self.verticalLayout.setStretch(1, 10)

        self.retranslateUi(Msg)
        QtCore.QMetaObject.connectSlotsByName(Msg)

    def retranslateUi(self, Msg):
        _translate = QtCore.QCoreApplication.translate
        Msg.setWindowTitle(_translate("Msg", "消息提示"))
        self.lbl_title.setText(_translate("Msg", "登入"))
        self.btn_minimized.setText(_translate("Msg", "0"))
        self.btn_close.setText(_translate("Msg", "r"))
        self.lbl_content.setText(_translate("Msg", "請先登入會員"))
        self.btn_confirm.setText(_translate("Msg", "確認"))

