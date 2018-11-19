from PyQt5.QtWidgets import QMainWindow
import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
import requests
from bs4 import BeautifulSoup
import re

s = requests.Session()


class Main(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()

    def load():
        floor = MainWindow.cbox.currentText()
        print(floor)

        #Sqe=1 -> 3F     Seq=2 -> 1F
        if floor == '3F':
            url = 'http://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst=2018/11/24'
        else:
            url = 'http://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=2&dateLst=2018/11/24'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        r = s.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', id='ctl00_ContentPlaceHolder1_tab1')

        td = re.compile('>(.*?)</td>')
        dat = re.findall(td, str(table))

        i = 0
        for row in range(0, 15):
            for col in range(0, 8):
                if dat[i].startswith('<a'):
                    a = re.search('''14dot1b.gif"/?> \((\d{,2})\)<''', dat[i]) #o
                    b = re.search('''actn010_2.gif"/?> \((\d{,2})\)<''', dat[i]) #v

                    if a and b:
                        dat[i] = 'ｏ{} ✓{}'.format(a[1], b[1])
                    elif a:
                        dat[i] = 'ｏ{}'.format(a[1])
                    elif b:
                        dat[i] = '✓{}'.format(b[1])

                MainWindow.tableWidget.item(row, col).setText(dat[i])
                i += 1


    MainWindow.btn.clicked.connect(load)
    sys.exit(app.exec_())
