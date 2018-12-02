from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
import MainWindow
import LoginWindow
import RegWindow
import sys
import datetime
from SportCenter import SportCenter, PATH_TO_AC, FILENAME


class Main(QMainWindow, MainWindow.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.show()
		self.week = 0
		self.setupUi(self)
		self.btn.clicked.connect(self.load)
		self.tableWidget.cellDoubleClicked.connect(self.cell_on_click)
		self.lbl_next.mousePressEvent = self.label_next
		self.lbl_previous.mousePressEvent = self.label_previous
		self.actionLogin.triggered.connect(self.login)
		self.actionExit.triggered.connect(self.close)

		self.Log = Login()
		self.Reg = Register()
		self.link = ''

		user = sc.auto_login()
		if user:
			self.lbl_status.setText('{}'.format(user))

	def load(self, date):
		if date == False:
			date = datetime.date.today()
		floor = self.cbox.currentText()
		print(floor, date)
		data = sc.parse_timetable(sc.get_timetable(floor, date))
		self.update_table_items(self.tableWidget, data)

	def update_table_items(self, widget, data):
		i = 0
		for row in range(0, 15):
			for col in range(0, 8):
				self.tableWidget.item(row, col).setText(data[i])
				i += 1
			app.processEvents()
			# This one is needed for updating text on mac
			# I dont know why

	def cell_on_click(self, row, column):
		print('({}, {})'.format(row, column))
		print(self.tableWidget.item(row, column).text())
		if sc.orderlink.get((row, column)):
			self.link = sc.orderlink[(row, column)]
			comfirm = sc.reg_confirm(self.link)
			for row in range(1, 15):
				self.Reg.tableWidget.item(row, 1).setText(comfirm[row-1])
			self.reg()

	def label_next(self, _):
		self.week += 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		self.load(date)

	def label_previous(self, _):
		self.week -= 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		self.load(date)

	def login(self):
		self.Log.show()

	def reg(self):
		self.Reg.show()


class Login(QMainWindow, LoginWindow.Ui_LoginWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.btn_login.clicked.connect(self.login)
		self.btn_cancel.clicked.connect(self.close)

	def login(self):
		username = self.tb_user.text()
		password = self.tb_pass.text()
		sc.username = username
		sc.password = password
		if username == "" or password == "":
			print("Username or Password empty")
			# Do something
		print(username, password)
		user = sc.login()
		if user:
			MainWindow.lbl_status.setText('{}'.format(user))
			self.hide()
		else:
			print('密碼錯誤')


class Register(QMainWindow, RegWindow.Ui_RegWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.tableWidget.setSpan(0, 0, 1, 2)
		self.btn_cancel.clicked.connect(self.close)
		self.btn_order.clicked.connect(self.order)

	def order(self):
		link = MainWindow.link
		sc.reg_order(link)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	sc = SportCenter()

	MainWindow = Main()
	sys.exit(app.exec_())
