from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import MainWindow
import sys
import requests
from bs4 import BeautifulSoup
import re
import datetime
from SportCenter import SportCenter

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

	def load(self, date):
		date = datetime.date.today() if date == False else date
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
		data = {'user': self.tb_user.text(), 'pass': self.tb_pass.text(), 'Submit': '登入'}
		print(data['user'], data['pass'])
		user = sc.login(data)

		if user:
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
	MainWindow = Main()
	sc = SportCenter()
	sys.exit(app.exec_())
