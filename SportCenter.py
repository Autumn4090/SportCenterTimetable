import requests
from bs4 import BeautifulSoup
import re


class SportCenter():
	"""
		# Todo: Add login function
		# Todo: Add next week function (Done)
		# Todo: Add register function
	"""

	def __init__(self):
		self.s = requests.session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
		self.root_url = 'http://info2.ntu.edu.tw'
		self.orderlink = dict()

	def get_timetable(self, floor, date='2018/11/24'):
		"""
			placeSeq=1 -> 3F
			placeSeq=2 -> 1F
		"""
		if floor == '3F':
			url = self.root_url + '/facilities/PlaceGrd.aspx?nFlag=0&placeSeq={}&dateLst={}'.format(1, date)
		else:
			url = self.root_url + '/facilities/PlaceGrd.aspx?nFlag=0&placeSeq={}&dateLst={}'.format(2, date)
		soup = BeautifulSoup(self.s.get(url).text, 'html.parser')
		table = soup.find('table', id='ctl00_ContentPlaceHolder1_tab1')
		return table

	def parse_timetable(self, timetable):
		"""

		"""
		td = re.compile('>(.*?)</td>')
		data = re.findall(td, str(timetable))
		i = 0
		for row in range(0, 15):
			for col in range(0, 8):
				if data[i].startswith('<a'):
					# print(data[i])
					a = re.search('''14dot1b.gif"/?> ?\((\d{,3})\)<''', data[i]) #o
					b = re.search('''actn010_2.gif"/?> ?\((\d{,3})\)<''', data[i]) #v
					c = re.search('''#696969">(.*?)<''', data[i]) #現場訂位

					if "預約" in data[i]:
						d = re.search('''<img alt="預約" id="btnOrder" onclick="javascript:location.href='(.*?)'" ''', data[i])
						self.orderlink[(row, col)] = d[1].replace('&amp;', '&').replace('§', '&sect')

					if a and b:
						data[i] = 'ｏ{} ✓{}'.format(a[1], b[1])
					elif a and c:
						data[i] = 'ｏ{}\n{}'.format(a[1], c[1])
					elif a:
						data[i] = 'ｏ{}'.format(a[1])
					elif b:
						data[i] = '✓{}'.format(b[1])
				i += 1
		return data

	def login(self, data):
		url_session = 'https://info2.ntu.edu.tw/facilities/SessionLogin.aspx'
		_ = self.s.get(url_session) # get session

		url_log = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
		soup = BeautifulSoup(self.s.post(url_log, data).text, 'html.parser')
		check = soup.find('span', id='ctl00_lblShow')
		if check:
			print(check)
