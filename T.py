from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QLabel, QLineEdit
import MainWindow
import RegWindow
import sys
import time
import datetime
from SportCenter import SportCenter
from SportCenterThreads import GetTimeTableThread, LoginThread


class Main(QMainWindow, MainWindow.Ui_MainWindow):
	"""

	"""
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.setWindowIcon(QtGui.QIcon('Gui/dev.ico'))
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

		size = self.geometry()
		screen = QDesktopWidget().screenGeometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
		self.show()
		self.lbl_refresh.mousePressEvent = self.refresh
		self.lbl_next.mousePressEvent = self.label_next
		self.lbl_previous.mousePressEvent = self.label_previous
		self.tableWidget.cellDoubleClicked.connect(self.cell_on_click)
		self.tableWidget_status.cellDoubleClicked.connect(self.status_update)
		self.btn_login.clicked.connect(self.login)
		self.tb_pass.returnPressed.connect(self.btn_login.click)

		self.week = 0
		self.selectedLink = ''
		self.RegWindow = Register()

		# Create Thread
		self.get_timetable_thread = GetTimeTableThread(sc)
		# Connect the signal to update table function
		self.get_timetable_thread.sig.connect(self._thread_update_table_items)

		self.login_thread = LoginThread(sc)
		# Connect the signal to update table function
		self.login_thread.sig.connect(self._after_login)

		sc.load_account()
		if sc.save:
			self.cb_savepass.setChecked(True)
			self.tb_user.setText(sc.username)
			self.tb_pass.setText(sc.password)

	def refresh(self, _, date=None):
		sc.clickable = dict()
		sc.orderlink = dict()

		self.table_initialize()
		if date is None:
			self.week = 0
			date = datetime.date.today()

		# Start the thread
		self.get_timetable_thread.start(date)

	def table_initialize(self):
		for row in range(1, 15):
			for col in range(1, 15):
				brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
				brush.setStyle(QtCore.Qt.NoBrush)
				self.tableWidget.item(row, col).setForeground(brush)
				self.tableWidget.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', 8))

	def _thread_update_table_items(self, data):
		self.update_table_items(self.tableWidget, data)

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
		if self.week == 0:
			return
		self.week -= 1
		date = str(datetime.date.today() + datetime.timedelta(days=self.week * 7))
		self.refresh(_, date)

	def cell_on_click(self, row, col):
		# print(row, col)
		# self.tableWidget.item(row, col).setText('({}, {})'.format(row, col))
		if sc.clickable.get((row, col)) is None:
			return
		elif not sc.is_login:
			self.tb_user.setFocus()
			return

		self.selectedLink = sc.orderlink[(row, col)]
		details = sc.reg_details(self.selectedLink)
		for row in range(1, 15):
			self.RegWindow.tableWidget.item(row, 1).setText(details[row-1])

		img = QtGui.QImage()
		assert img.loadFromData(sc.get_captcha())
		recap = QLabel()
		recap.setAlignment(QtCore.Qt.AlignCenter)
		recap.setPixmap(QtGui.QPixmap().fromImage(img))
		self.RegWindow.tableWidget.setCellWidget(15, 0, recap)

		self.show_reg()

	def login(self):
		username = self.tb_user.text()
		password = self.tb_pass.text()
		sc.username = username
		sc.password = password
		if username == '' and password == '':
			print('Username and password empty')
			# Do something
		print(username, password)
		sc.save = self.cb_savepass.isChecked()
		self.login_thread.start()

	def _after_login(self, user):
		if user:
			self.tb_user.hide()
			self.tb_pass.hide()
			self.btn_login.hide()
			self.cb_savepass.hide()
			self.lbl_userstatus.setText('{}'.format(user.upper()))
			self.status_update()
			self.refresh('')
		else:
			print('登入失敗')

	def status_update(self):
		# print(row, col)
		# self.tableWidget_status.item(row, col).setText('({}, {})'.format(row, col))
		if sc.is_login:
			data = sc.status()
			for row in range(1,20):
				for col in range(0,5):
					self.tableWidget_status.item(row, col).setText(data[row-1][col])

	def show_reg(self):
		self.RegWindow.show()


class Register(QMainWindow, RegWindow.Ui_RegWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

		size = self.geometry()
		screen = QDesktopWidget().screenGeometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

		self.tableWidget.setSpan(0, 0, 1, 2)
		self.btn_cancel.clicked.connect(self.close)
		self.btn_order.clicked.connect(self.order)

		self.res = QLineEdit()
		self.res.setText('')
		self.res.setAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.setCellWidget(15, 1, self.res)
		# just test

		self.tableWidget.item(0,15)

	def order(self):
		link = MainWindow.selectedLink
		validateCode = self.res.text()
		# sc.reg_order(link, validateCode)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	sc = SportCenter()

	MainWindow = Main()
	sys.exit(app.exec_())
