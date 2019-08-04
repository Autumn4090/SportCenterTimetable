from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDesktopWidget, QLabel, QLineEdit
import MainWindow
import RegWindow
import MsgWidget
import sys
import time
import datetime
from SportCenter import SportCenter
from SportCenterThreads import GetTimeTableThread, LoginThread
import threading
# import cgitb
# cgitb.enable(format='text') # Avoid MainWindow crashing


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
		self.tableWidget_status.cellDoubleClicked.connect(self.resign)
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

		self.heartbeatLoop = threading.Thread(target=sc.heartbeat)

		sc.load_account()
		if sc.save:
			self.cb_savepass.setChecked(True)
			self.tb_user.setText(sc.username)
			self.tb_pass.setText(sc.password)

		self.widget = QWidget()
		self.notify = MsgBox(parent=self.widget)

	def msg(self, title, content, timeout=5000):
		self.notify.show(title=title, content=content, timeout=timeout).showAnimation()

	def refresh(self, _, date=None):
		sc.regLink = dict()
		sc.regClickable = dict()

		self.table_initialize(self.tableWidget, (1,15), (1,15), 8)
		if date is None:
			self.week = 0
			date = datetime.date.today()

		# Start the thread
		self.get_timetable_thread.start(date)

	def table_initialize(self, widget, r, c, fontsize):
		for row in range(r[0], r[1]):
			for col in range(c[0], c[1]):
				brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
				brush.setStyle(QtCore.Qt.NoBrush)
				widget.item(row, col).setForeground(brush)
				widget.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', fontsize))

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

					if sc.regClickable.get((row, col)):
						brush = QtGui.QBrush(QtGui.QColor(50, 215, 50))
						self.tableWidget.item(row, col).setForeground(brush)
						self.tableWidget.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', 8, QtGui.QFont.Bold))
					i += 1
		self.lbl_loadingtime.setText(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()))
		self.msg(' ', '加載完成', 1500)

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
		if sc.regClickable.get((row, col)) is None:
			return
		elif not sc.is_login:
			self.tb_user.setFocus()
			return

		self.selectedLink = sc.regLink[(row, col)]
		details = sc.reg_details(self.selectedLink)
		for row in range(1, 15):
			self.RegWindow.tableWidget.item(row, 1).setText(details[row-1])

		self.Reg.valid_update(sc.get_captcha())
		self.reg()

	def login(self):
		username = self.tb_user.text()
		password = self.tb_pass.text()
		sc.username = username
		sc.password = password
		if username == '' and password == '':
			self.msg('空白','帳號及密碼不能為空')
			#print('Username and password empty')
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
			self.heartbeatLoop.start()
			self.msg('歡迎', '{}'.format(user.upper()))
			# self.refresh(0)
		else:
			self.msg('登入失敗', '如同你的人生一樣失敗')
			#print('登入失敗')

	def status_update(self):
		# print(row, col)
		# self.tableWidget_status.item(row, col).setText('({}, {})'.format(row, col))
		if sc.is_login:
			sc.resLink = dict()
			sc.resClickable = dict()
			self.table_initialize(self.tableWidget_status, (1,20), (0,5), 6)
			data = sc.status()
			for row in range(1,20):
				for col in range(0,5):
					self.tableWidget_status.item(row, col).setText(data[row][col+1])

					if sc.resClickable.get((row, col)):
						brush = QtGui.QBrush(QtGui.QColor(50, 215, 50))
						self.tableWidget_status.item(row, col).setForeground(brush)
						self.tableWidget_status.item(row, col).setFont(QtGui.QFont('Microsoft JhengHei', 6, QtGui.QFont.Bold))
			self.msg(' ', '加載完成', 1500)
			#print('updated')

	def show_reg(self):
		self.RegWindow.show()

	def resign(self, row ,col):
		if sc.resClickable.get((row, col)) is None:
			return
		elif not sc.is_login:
			self.tb_user.setFocus()
			return

		self.resNum = sc.resLink[(row, col)]
		print(self.resNum)
		sc.res_details(self.resNum) # pop box confirm
		sc.res_post(self.resNum)
		self.status_update()


class Register(QMainWindow, RegWindow.Ui_RegWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

		size = self.geometry()
		screen = QDesktopWidget().screenGeometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

		self.tableWidget.setSpan(0, 0, 1, 2)
		self.tableWidget.cellClicked.connect(self._valid)
		self.btn_cancel.clicked.connect(self.close)
		self.btn_order.clicked.connect(self.order)

	def _valid(self, row, col):
		if (row, col) == (15, 0):
			self.valid_update(sc.get_captcha())

	def valid_update(self, code):
		# Captcha image
		captcha = QtGui.QImage()
		assert captcha.loadFromData(code)
		self.capImg = QLabel()
		self.capImg.setAlignment(QtCore.Qt.AlignCenter)
		self.capImg.setPixmap(QtGui.QPixmap().fromImage(captcha))
		self.tableWidget.setCellWidget(15, 0, self.capImg)

		# InputBox
		self.capBox = QLineEdit()
		self.capBox.setText('')
		self.capBox.setAlignment(QtCore.Qt.AlignCenter)
		self.tableWidget.setCellWidget(15, 1, self.capBox)

	def order(self):
		link = MainWindow.selectedLink
		validateCode = self.capBox.text()
		print(validateCode)
		sc.reg_post(link, validateCode)
		self.close()


class MsgBox(QWidget, MsgWidget.Ui_Msg):
	SignalClosed = QtCore.pyqtSignal()
	def __init__(self, title='', content='', timeout=0, *args, **kwargs):
		super(MsgBox, self).__init__(*args, **kwargs)
		self.setupUi(self)
		self.setTitle(title).setContent(content).setIcon()
		self._timeout = timeout
		self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint |
							QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

		self.btn_close.clicked.connect(self.onClose)
		self.btn_confirm.clicked.connect(self.onConfirm)

		self.desktop = QApplication.instance().desktop()
		self.startPos = QtCore.QPoint(
			self.desktop.screenGeometry().width(),
			self.desktop.availableGeometry().height() - self.height() - 25
		)
		self.endPos = QtCore.QPoint(
			self.desktop.screenGeometry().width() - self.width() - 5,
			self.desktop.availableGeometry().height() - self.height() - 25
		)
		self.move(self.startPos)

		self.animation = QtCore.QPropertyAnimation(self, b"pos") ##
		self.animation.finished.connect(self.onAnimationEnd)
		self.animation.setDuration(250) # speed

		self._timer = QtCore.QTimer(self, timeout=self.closeAnimation)

	def setTitle(self, title):
		if title:
			self.lbl_title.setText(title)
		return self

	def setContent(self, content):
		if content:
			self.lbl_content.setText(content)
		return self

	def setIcon(self):
		self.lbl_icon.setPixmap(QtGui.QPixmap('Gui/dev.ico').scaled(80, 80))
		return self

	def setTimeout(self, timeout):
		if isinstance(timeout, int):
			self._timeout = timeout
		return self

	def onClose(self):
		self.closeAnimation()
		# QTimer.singleShot(100, self.closeAnimation)

	def onConfirm(self):
		self.is_confirm = True # !! Resign confirm
		self.closeAnimation()

	def show(self, title='', content='', timeout=5000):
		self._timer.stop()
		self.hide()
		self.move(self.startPos)  # Initialize position to bottom right corner
		super(MsgBox, self).show()
		self.setTitle(title).setContent(content).setTimeout(timeout)
		return self

	def showAnimation(self):
		#print("showAnimation isShow = True")
		# Show animation
		self.isShow = True
		self.animation.stop() # Stop previous animation and restart
		self.animation.setStartValue(self.pos())
		self.animation.setEndValue(self.endPos)
		self.animation.start()
		self._timer.start(self._timeout)
		# QTimer.singleShot(self._timeout, self.closeAnimation)

	def closeAnimation(self):
		# Close animation
		self.isShow = False
		self.animation.stop()
		self.animation.setStartValue(self.pos())
		self.animation.setEndValue(self.startPos)
		self.animation.start()

	def onAnimationEnd(self):
		# End animation
		#print("onAnimationEnd isShow", self.isShow)
		if not self.isShow:
			#print("onAnimationEnd close()")
			self.close()
			#print("onAnimationEnd stop timer")
			self._timer.stop()
			#print("onAnimationEnd close and emit signal")
			self.SignalClosed.emit()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	sc = SportCenter()

	MainWindow = Main()
	sys.exit(app.exec_())
