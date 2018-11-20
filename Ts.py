from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import MainWindow
import sys
import requests
from bs4 import BeautifulSoup
import re
from SportCenter import SportCenter

s = requests.Session()


class Main(QMainWindow, MainWindow.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.btn.clicked.connect(self.load)
		# self.tableWidget.doubleClicked.connect(self.on_click)
		# self.tableWidget.itemChanged.connect(self.on_click)
		# self.tableWidget.cellClicked.connect(self.on_click)

	def load(self):
		floor = self.cbox.currentText()
		print(floor)
		data = sc.parse_timetable(sc.get_timetable(floor))
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

	def on_click(self, row ,column):
		# Not working
		print(self.tableWidget.itemAt(row, column).text())

	def main(self):
		pass


if __name__ == "__main__":
	app = QApplication(sys.argv)
	MainWindow = Main()
	MainWindow.show()

	sc = SportCenter()
	sys.exit(app.exec_())
