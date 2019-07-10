from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import MainWindow
import sys
import time
import datetime
from SportCenter import SportCenter


class Main(QMainWindow, MainWindow.Ui_MainWindow):
	"""

	"""
	def __init__(self):
		super(self.__class__, self).__init__()
		self.show()
		self.setupUi(self)
		self.lbl_refresh.mousePressEvent = self.refresh
		self.lbl_next.mousePressEvent = self.label_next
		self.lbl_previous.mousePressEvent = self.label_previous
		self.tableWidget.cellDoubleClicked.connect(self.cell_on_click)
		self.btn_login.clicked.connect(self.login)

		self.week = 0
		self.selectedLink = ''
		self.tableWidget_status.cellDoubleClicked.connect(self.status_update)

	def refresh(self, _, date=None):
		sc.clickable = dict()
		sc.orderlink = dict()

		self.table_initialize()
		if date is None:
			self.week = 0
			date = datetime.date.today()
		data = sc.get_timetable(date)
		self.update_table_items(self.tableWidget, data)
		sc.status()

	def table_initialize(self):
		for row in range(1, 15):
			for col in range(1, 15):
				brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
				brush.setStyle(QtCore.Qt.NoBrush)
				self.tableWidget.item(row, col).setForeground(brush)
				self.tableWidget.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', 8))

	def update_table_items(self, widget, data):
		for runtime in range(1, 3):
			i = 1
			for row in range(0, 15):
				for col in range(runtime, 15, 2):
					if i % 8 == 0:
						i += 1
					self.tableWidget.item(row, col).setText(data[runtime-1][i])

					if sc.clickable.get((row, col)):
						brush = QtGui.QBrush(QtGui.QColor(50, 215, 50))
						self.tableWidget.item(row, col).setForeground(brush)
						self.tableWidget.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', 8, QtGui.QFont.Bold))
					i += 1
		self.lbl_loadingtime.setText(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()))

	def label_next(self, _):
		self.week += 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		self.refresh(_, date)

	def label_previous(self, _):
		self.week -= 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		self.refresh(_, date)

	def cell_on_click(self, row, col):
		# print(row, col)
		# self.tableWidget.item(row, col).setText('({}, {})'.format(row, col))
		if sc.clickable.get((row, col)) is None:
			return

		self.selectedLink = sc.orderlink[(row, col)]
		print(self.selectedLink)

	def login(self):
		username = self.tb_user.text()
		password = self.tb_pass.text()
		sc.username = username
		sc.password = password
		if username == '' and password == '':
			print('Username and password empty')
			# Do something
		print(username, password)
		user = sc.login()
		if user:
			self.tb_user.hide()
			self.tb_pass.hide()
			self.btn_login.hide()
			self.lbl_userstatus.setText('{}'.format(user.upper()))
			self.status_update()
			# self.refresh(0)
		else:
			print('登入失敗')

	def status_update(self):
		# print(row, col)
		# self.tableWidget_status.item(row, col).setText('({}, {})'.format(row, col))
		data = sc.status()
		for row in range(1,20):
			for col in range(0,5):
				self.tableWidget_status.item(row, col).setText(data[row-1][col])



if __name__ == "__main__":
	app = QApplication(sys.argv)
	sc = SportCenter()

	MainWindow = Main()
	sys.exit(app.exec_())