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
		self.setupUi(self)
		self.btn.clicked.connect(self.load)
		self.tableWidget.cellDoubleClicked.connect(self.on_click)
		# self.tableWidget.itemChanged.connect(self.on_click)
		# self.tableWidget.cellClicked.connect(self.on_click)
		self.week = 0
		self.lbl_next.mouseReleaseEvent = self.label_next
		self.lbl_previous.mouseReleaseEvent = self.label_previous
		self.actionLogin.triggered.connect(self.login)
		self.actionExit.triggered.connect(self.close)

	def load(self, date=''):
		if not date: # is it possible to code more beauty
			self.week = 0 #
			date = str(datetime.date.today()) #

		floor = self.cbox.currentText()
		print(floor)
		data = sc.parse_timetable(sc.get_timetable(floor, date))
		self.connect_table_items(self.tableWidget, data)

	def connect_table_items(self, widget, data):
		i = 0
		for row in range(0, 15):
			for col in range(0, 8):
				self.tableWidget.item(row, col).setText(data[i])
				# This one is need for updating text on mac
				# I dont know why
				app.processEvents()
				i += 1

	def on_click(self, row, column):
		print(self.tableWidget.item(row, column).text())

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
		print('Login Test')

	def main(self):
		pass


if __name__ == "__main__":
	app = QApplication(sys.argv)
	MainWindow = Main()
	MainWindow.show()

	sc = SportCenter()
	sys.exit(app.exec_())
