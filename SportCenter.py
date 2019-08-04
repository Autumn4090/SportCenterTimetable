import requests
from bs4 import BeautifulSoup
import re
import os
import configparser
import time

path = 'C:/Users/' + os.getlogin() + '/Documents/Configuration'
filename = 'conf.ini'


class SportCenter():
	def __init__(self):
		self.s = requests.session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
		self.root_url = 'http://ntupesc.ntu.edu.tw'
		self.username = str()
		self.password = str()
		self.is_login = False
		self.save = False
		self.regLink = dict()
		self.regClickable = dict()
		# a map for storeing the bookable cells
		self.resLink = dict()
		self.resClickable = dict()

	def heartbeat(self):
		url = self.root_url + '/facilities/'
		while not self.is_login:
			time.sleep(1)

		while self.is_login:
			try:
				self.s.head(url)
				print('心跳...')
				time.sleep(300)
			except requests.ConnectionError:
				print('請檢查網絡狀態')
			except:
				print('請聯系開發者')

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
						self.regLink[(row, col)] = d[1].replace('&amp;', '&').replace('§', '&sect')
						self.regClickable[(row, col)] = True

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
		url_session = 'https://ntupesc.ntu.edu.tw/facilities/SessionLogin.aspx' # notice: https
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
		config.add_section('save')
		config.add_section('account')
		if 'conf.ini' not in os.listdir(path) or not self.save:
			config['save']['on/off'] = '0'
			config['account']['username'] = ''
			config['account']['password'] = ''
		else:
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
		td = re.compile('''</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)            </td><td>.*      </td><td>(.*)</td><td>.*            </td><td>(.*)</td><td><input ''')
		data = re.findall(td, self.s.get(url).text)
		data.insert(0, ['' for k in range(6)])

		for row in range(len(data)):
			col = 4
			if "預約" in data[row][5]:
				self.resLink[(row, col)] = data[row][0]
				self.resClickable[(row, col)] = True
				# print(self.resLink, self.resClickable)
		return data[0:20]

	def reg_details(self, link):
		url = self.root_url + '/facilities/' + link
		print(url)

		web = self.s.get(url).text
		details = [re.search('''lblbookSeq.*>(.*?)<''', web)[1],
				   re.search('''lblplaceName.*>(.*?)            <''', web)[1],
				   re.search('''spanFrontMark['"]>(.*?)<''', web)[1],
				   re.search('''lblmemberName.*>(.*?)<''', web)[1],
				   '',
				   '',
				   '',
				   '{}@ntu.edu.tw'.format(self.username),
				   re.search('''lblPayType.*>(.*?)<''', web)[1],
				   '現金',
				   re.search('''lblDate.*>(.*?)<''', web)[1],
				   '{}:00 至 {}:00'.format(re.search('''hidsTime.*['"](\d{1,2})''', web)[1],
										  re.search('''hideTime.*['"](\d{1,2})''', web)[1]),
				   re.search('''txtPlaceNum.*['"](\d{1,})''', web)[1],
				   re.search('''lblPayStand.*>(\$NT\d{,3})''', web)[1]]


		self.regformdata = {'VIEWSTATE':       re.search('''__VIEWSTATE.*value=['"](.*?)['"]''', web)[1],
						 'EVENTVALIDATION': re.search('''__EVENTVALIDATION.*value=['"](.*?)['"]''', web)[1],
						 'TimeStart':     re.search('''hidsTime.*['"](\d{1,2})''', web)[1],
						 'TimeEnd':       re.search('''hideTime.*['"](\d{1,2})''', web)[1],
						 'hidbookDate':   re.search('''hidbookDate.*value=['"](.*?)['"]''', web)[1],
						 'hidpayPrice':   re.search('''hidpayPrice.*value=['"](.*?)['"]''', web)[1],
						 'hidpeekCharge': re.search('''hidpeekCharge.*value=['"](.*?)['"]''', web)[1],
						 'hidoffCharge':  re.search('''hidoffCharge.*value=['"](.*?)['"]''', web)[1],
						 'hidWeek':       re.search('''hidWeek.*value=['"](.*?)['"]''', web)[1],
						 'hiddateLst':    re.search('''hiddateLst.*value=['"](.*?)['"]''', web)[1]}

		return details

	def reg_post(self, link, code):
		url = self.root_url + '/facilities/' + link
		data = {'__EVENTTARGET':     '',
				'__EVENTARGUMENT':   '',
				'__LASTFOCUS':       '',
				'__VIEWSTATE':       self.regformdata['VIEWSTATE'],
				'__EVENTVALIDATION': self.regformdata['EVENTVALIDATION'],

				'ctl00$ContentPlaceHolder1$txtContactName':   '',
				'ctl00$ContentPlaceHolder1$txtContactTel':    '',
				'ctl00$ContentPlaceHolder1$txtFax':           '',
				'ctl00$ContentPlaceHolder1$txtEmail':         '{}@ntu.edu.tw'.format(self.username),
				'ctl00$ContentPlaceHolder1$DropLstPayMethod': '現金',
				'ctl00$ContentPlaceHolder1$txtpayHourNum':    '',
				'ctl00$ContentPlaceHolder1$DropLstTimeStart': self.regformdata['TimeStart'], #
				'ctl00$ContentPlaceHolder1$DropLstTimeEnd':   self.regformdata['TimeEnd'], #
				'ctl00$ContentPlaceHolder1$txtPlaceNum':      '1',
				'ctl00$ContentPlaceHolder1$txtValidateCode':  '{}'.format(code),
				'ctl00$ContentPlaceHolder1$btnOrder':         '送出預約',
				'ctl00$ContentPlaceHolder1$hidbookDate':      self.regformdata['hidbookDate'], #
				'ctl00$ContentPlaceHolder1$hidmemberId':      '{}'.format(self.username),
				'ctl00$ContentPlaceHolder1$hidplaceSeq':      '1',
				'ctl00$ContentPlaceHolder1$hidpayPrice':      self.regformdata['hidpayPrice'], #
				'ctl00$ContentPlaceHolder1$hidpeekCharge':    self.regformdata['hidpeekCharge'], #
				'ctl00$ContentPlaceHolder1$hidoffCharge':     self.regformdata['hidoffCharge'], #
				'ctl00$ContentPlaceHolder1$hidsTime':         self.regformdata['TimeStart'], #
				'ctl00$ContentPlaceHolder1$hideTime':         self.regformdata['TimeEnd'], #
				'ctl00$ContentPlaceHolder1$hidWeek':          self.regformdata['hidWeek'],
				'ctl00$ContentPlaceHolder1$hiddateLst':       self.regformdata['hiddateLst']}

		print(data)
		result = self.s.post(url, data=data)
		print(result.text)
		if '成功' in result.text:
			print('成功')

	def get_captcha(self):
		url = self.root_url + '/facilities/ValidateCode.aspx?ImgID=Login'
		rec = self.s.get(url).content
		return rec

	def res_details(self, num):
		url = self.root_url + '/facilities/PlaceOrderMemLst.aspx?bookSeq=' + num
		web = self.s.get(url).text
		self.resformdata = {'VIEWSTATE':       re.search('''__VIEWSTATE.*value=['"](.*?)['"]''', web)[1],
							'EVENTVALIDATION': re.search('''__EVENTVALIDATION.*value=['"](.*?)['"]''', web)[1],
							'hidfldmemberId': re.search('''hidfldmemberId.*value=['"](.*?)['"]''', web)[1],
							'hidfldpoints':   re.search('''hidfldpoints.*value=['"](.*?)['"]''', web)[1],
							'hidfldplaceSeq': re.search('''hidfldplaceSeq.*value=['"](.*?)['"]''', web)[1]}
		print(self.resformdata)

	def res_post(self, num):
		url = self.root_url + '/facilities/PlaceOrderMemLst.aspx?bookSeq=' + num
		# self.res_details()

		data = {'__EVENTTARGET':     '',
				'__EVENTARGUMENT':   '',
				'__VIEWSTATE':       self.resformdata['VIEWSTATE'],
				'__EVENTVALIDATION': self.resformdata['EVENTVALIDATION'],

				'ctl00$ContentPlaceHolder1$hidfldmemberId': self.resformdata['hidfldmemberId'],
				'ctl00$ContentPlaceHolder1$hidfldpoints':   self.resformdata['hidfldpoints'],
				'ctl00$ContentPlaceHolder1$hidfldplaceSeq': self.resformdata['hidfldplaceSeq'],
				'ctl00$ContentPlaceHolder1$btnCancelOrder': '取消預約'}

		result = self.s.post(url, data=data)
		print(result.text)
