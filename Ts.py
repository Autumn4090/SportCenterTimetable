from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import MainWindow
import sys
import requests
from bs4 import BeautifulSoup
import re
import datetime
from SportCenter import SportCenter, PATH_TO_AC, FILENAME

s = requests.Session()

class Main(QMainWindow, MainWindow.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.show()
		self.week = 0
		self.setupUi(self)
		self.btn.clicked.connect(self.load)
		self.tableWidget.cellPressed.connect(self.on_click)
		# self.tableWidget.itemChanged.connect(self.on_click)
		# self.tableWidget.cellClicked.connect(self.on_click)
		self.lbl_next.mousePressEvent = self.label_next
		self.lbl_previous.mousePressEvent = self.label_previous
		self.actionLogin.triggered.connect(self.login)
		self.btn_login.clicked.connect(self.login)
		# self.actionLogin.triggered.connect(self.login)
		self.actionExit.triggered.connect(self.close)
		user = sc.auto_login()
		if user:
			self.update_login(user)


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

	def on_click(self, row, column):
		print('({}, {})'.format(row, column))
		print(self.tableWidget.item(row, column).text())
		if (row, column) in sc.orderlink.keys():
			print(sc.orderlink[(row, column)])
			sc.register(sc.orderlink[(row, column)])

	def label_next(self, _):
		self.week += 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		print('Today:{} Next:{}'.format(datetime.date.today(), date))
		self.load(date)

	def label_previous(self, _):
		self.week -= 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		print('Today:{} Next:{}'.format(datetime.date.today(), date))
		self.load(date)

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
		self.update_login(user)

	def update_login(self, user):
		if user:
			sc.store_account(PATH_TO_AC, FILENAME)
			self.horizontalLayoutWidget.setGeometry(QtCore.QRect(620, 750, 441, 51)) # lazy reuse the lbl_user
			self.lbl_user.setText('{}'.format(user))
			self.lbl_pass.hide()
			self.tb_user.hide()
			self.tb_pass.hide()
			self.btn_login.hide()
		else:
			print('密碼錯誤')


	def main(self):
		pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	sc = SportCenter()

	MainWindow = Main()
	sys.exit(app.exec_())
