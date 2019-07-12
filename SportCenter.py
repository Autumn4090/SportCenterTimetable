import requests
from bs4 import BeautifulSoup
import re
import os
import configparser

path = 'C:/Users/' + os.getlogin() + '/Documents/Configuration'
filename = 'conf.ini'


class SportCenter():
	def __init__(self):
		self.s = requests.session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
		self.root_url = 'http://info2.ntu.edu.tw'
		self.username = str()
		self.password = str()
		self.is_login = False
		self.save = False
		self.orderlink = dict()
		self.clickable = dict()
		# a map for storeing the bookable cells

	def get_timetable(self, date):
		"""
			placeSeq=1 -> 3F
			placeSeq=2 -> 1F
		"""
		table = list()
		for floor in (2, 1):
			url = self.root_url + '/facilities/PlaceGrd.aspx?nFlag=0&placeSeq={}&dateLst={}'.format(floor, date)
			# soup = BeautifulSoup(self.s.get(url).text, 'html.parser')
			table.append(self.parse_timetable(self.s.get(url).text, floor))
		return table

	def parse_timetable(self, timetable, floor):
		"""

		"""
		td = re.compile('>(.*?)</td>')
		data = re.findall(td, str(timetable))
		color_map = {}
		i = 0
		# print(data)
		for row in range(0, 15):
			for col in range(0, 8):
				# print(data[i])
				if data[i].startswith('<a'):
					a = re.search('''14dot1b.gif['"].*?/> ?\((\d{,3})\)<''', data[i]) #o
					b = re.search('''actn010_2.gif['"].*?/> ?\((\d{,3})\)<''', data[i]) #v
					c = re.search('''#696969['"]>(.*?)<''', data[i]) #現場訂位

					if "預約" in data[i]:
						d = re.search('''onclick=javascript:location.href='(.*?)'>''', data[i])
						if floor == 2: # 1F
							col = col * 2 - 1
						else:
							col *= 2
						self.orderlink[(row, col)] = d[1].replace('&amp;', '&').replace('§', '&sect')
						self.clickable[(row, col)] = True

					if a and b:
						data[i] = 'ｏ{} ✓{}'.format(a[1], b[1])
					elif a and c:
						data[i] = 'ｏ{}\n{}'.format(a[1], c[1])
					elif a:
						data[i] = 'ｏ{}'.format(a[1])
					elif b:
						data[i] = '✓{}'.format(b[1])
				i += 1
		# print(data)
		return data

	def login(self):
		data = {'user': self.username, 'pass': self.password, 'Submit': '登入'}
		url_session = 'https://info2.ntu.edu.tw/facilities/SessionLogin.aspx' # notice: https
		self.s.get(url_session) # get COOKIES

		url_log = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
		soup = BeautifulSoup(self.s.post(url_log, data).text, 'html.parser')
		check = soup.find('span', id='ctl00_lblShow')
		if check:
			self.save_account()
			self.is_login = True
			return str(check)[67:-48]
		return check

	def save_account(self):
		config = configparser.ConfigParser()
		os.makedirs(path, exist_ok=True)
		if 'conf.ini' not in os.listdir(path) or not self.save:
			config.add_section('save')
			config.add_section('account')
			config['save']['on/off'] = '0'
			config['account']['username'] = ''
			config['account']['password'] = ''
		else:
			config.add_section('save')
			config.add_section('account')
			config['save']['on/off'] = '1'
			config['account']['username'] = self.username
			config['account']['password'] = self.password

		with open(os.path.join(path, filename), 'w') as f:
			config.write(f)

	def load_account(self):
		config = configparser.ConfigParser()
		os.makedirs(path, exist_ok=True)
		if 'conf.ini' in os.listdir(path):
			config.read(os.path.join(path, filename))
			self.save = config.getboolean('save', 'on/off')
			self.username = config.get('account', 'username')
			self.password = config.get('account', 'password')

	def status(self):
		url = self.root_url + '/facilities/PlaceMemberGrd.aspx'

		# 預約編號 (預約日期) (預約時段) (預約場地) 方式 (金額) 收據編號 (狀態)
		td = re.compile('''</td><td>.*</td><td>(.*)</td><td>(.*)</td><td>(.*)            </td><td>.*      </td><td>(.*)</td><td>.*            </td><td>(.*)</td><td><input ''')
		data = re.findall(td, self.s.get(url).text)
		return data[0:19]

