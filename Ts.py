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
		self.tableWidget.cellDoubleClicked.connect(self.on_click)

	def load(self):
		floor = self.cbox.currentText()
		print(floor)
		data = sc.parse_timetable(sc.get_timetable(floor))
		self.connect_table_items(self.tableWidget, data)

	def update_table_items(self, widget, data):
		i = 0
		for row in range(0, 15):
			for col in range(0, 8):
				self.tableWidget.item(row, col).setText(data[i])
				i += 1
			app.processEvents()
			# This one is needed for updating text on mac
			# I dont know why

	def on_click(self, row ,column):
		print(self, row, column)
		print(self.tableWidget.item(row, column).text())

	def main(self):
		pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	MainWindow = Main()
	MainWindow.show()

	sc = SportCenter()
	sys.exit(app.exec_())
