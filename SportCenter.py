import requests
from bs4 import BeautifulSoup
import re
import os

PATH_TO_AC = "C:\\Users\\Public\\Documents"
FILENAME = "Roaming"


class SportCenter():
	"""
		# Todo: Add login function (Done)
		# Todo: Add logout function
		# Todo: Add next week function (Done)
		# Todo: Add register function
		# Todo: Add cancel function
	"""

	def __init__(self):
		self.s = requests.session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
		self.root_url = 'http://info2.ntu.edu.tw'
		self.orderlink = dict()
		self.username = str()
		self.password = str()
		self.is_login = False
		self.clickable = dict()
		# a map for storeing the bookable cells

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
		color_map = {}
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
		return data

	def login(self):
		data = {'user': self.username, 'pass': self.password, 'Submit': '登入'}
		url_session = 'https://info2.ntu.edu.tw/facilities/SessionLogin.aspx'
		self.s.get(url_session) # get COOKIES

		url_log = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
		soup = BeautifulSoup(self.s.post(url_log, data).text, 'html.parser')
		check = soup.find('span', id='ctl00_lblShow')
		if check:
			self.store_account(PATH_TO_AC, FILENAME)
			self.is_login = True
			return str(check)[67:-48]
		return check

	def store_account(self, path, filename):
		# os.path.join(path, filename) is better than path + filename
		with open(os.path.join(path, filename), 'w+') as f:
			f.write('{},{}'.format(self.username, self.password))

	def read_account(self, path, filename):
		path_to_file = os.path.join(path, filename)
		if os.path.isfile(path_to_file):
			with open(path_to_file, 'r') as f:
				line = f.readline().strip().split(',')
				if len(line) == 1:
					return False
				self.username = line[0]
				self.password = line[1]
				if self.username == "" or self.password == "":
					return False
				return True
		else:
			return False

	def auto_login(self):
		if self.read_account(PATH_TO_AC, FILENAME):
			return self.login()
		else:
			return False

	def reg_confirm(self, link):
		url = self.root_url + '/facilities/' + link
		print(url)
		soup = BeautifulSoup(self.s.get(url).text, 'html.parser')
		# table = soup.find('table', class_='table')
		confirm = [soup.find('span', id='ctl00_ContentPlaceHolder1_lblbookSeq').string,
				    soup.find('span', id='ctl00_ContentPlaceHolder1_lblplaceName').string,
				    soup.find('span', class_='spanFrontMark').string,
				    soup.find('span', id='ctl00_ContentPlaceHolder1_lblmemberName').string,
					'', # 'ctl00_ContentPlaceHolder1_txtContactName'
					'', # 'ctl00_ContentPlaceHolder1_txtContactTel'
					'', # 'ctl00_ContentPlaceHolder1_txtFax'
					'kw904@hotmail.com(搵細宏搞)', # 'ctl00_ContentPlaceHolder1_txtEmail'
					soup.find('span', id='ctl00_ContentPlaceHolder1_lblPayType').string,
					'現金',
					soup.find('span', id='ctl00_ContentPlaceHolder1_lblDate').string,
					'{}:00 至 {}:00'.format(soup.find('input', id='ctl00_ContentPlaceHolder1_hidsTime')['value'],
												soup.find('input', id='ctl00_ContentPlaceHolder1_hideTime')['value']),
					soup.find('input', id='ctl00_ContentPlaceHolder1_txtPlaceNum')['value'],
					re.search('(\$NT.*?\))', str(soup.find('span', id='ctl00_ContentPlaceHolder1_lblPayStand')))[0]]
		return confirm

	def reg_order(self, link):
		url = self.root_url + '/facilities/' + link
		print(url)
		soup = BeautifulSoup(self.s.get(url).text, 'html.parser')
		table = soup.find('table', class_='table')
		print(table)

		data = {'__EVENTTARGET': '',
				'__EVENTARGUMENT': '',
				'__LASTFOCUS': '',
				'__VIEWSTATE': '/wEPDwUKMTMxOTU0ODM0MQ9kFgJmD2QWAgIDD2QWCAIDDw8WAh4EVGV4dAUZ5LuK5pel5pel5pyf77yaMjAxOC8xMS8yMmRkAgUPDxYCHwAFb+S9v+eUqOiAhe+8muWKieW7uuWujyhiMDc1MDIxMzIpPEJSPui6q+S7veWIpe+8muWtuOeUnzxCUj7lt7LnmbvlhaU8QlI+PEJSPuatoei/juS9v+eUqOe3muS4iuWgtOWcsOmgkOe0hOezu+e1sWRkAgsPFgIfAAWcCjxtYXJxdWVlIHNjcm9sbGFtb3VudD0nMicgc2Nyb2xsZGVsYXk9JzEzMCcgZGlyZWN0aW9uPSAndXAnIGlkPXhpYW9xaW5nIG9ubW91c2VvdmVyPXhpYW9xaW5nLnN0b3AoKSBvbm1vdXNlb3V0PXhpYW9xaW5nLnN0YXJ0KCk+PHA+77yKMTEvMjYo5LqU77yJ5pmo57695aC05Zyw5Y+W5raIPGEgaHJlZj1qYXZhc2NyaXB0OnZvaWQod2luZG93Lm9wZW4oJ05ld3NGb3JtLmFzcHg/bmV3c0lkPTIzNScsJ+acgOaWsOa2iOaBrycsJ21lbnViYXI9bm8sc3RhdHVzPW5vLGRpcmVjdG9yaWVzPW5vLG1lbnViYXI9bm8scmVzaXphYmxlPW5vLHRvb2xiYXI9bm8sc2Nyb2xsYmFycz15ZXMsdG9wPTIwMCxsZWZ0PTIwMCx3aWR0aD01NTAsaGVpZ2h0PTMwMCcpKT4uLi5Nb3JlPC9hPiAg44CQMjAxOC8xMS8xOeabtOaWsOOAkTwvcD48cD7vvIoxMDflubQxMeaciOaZqOmWk+eQg+WgtCgwNjoxMH4wNzo1MCnloLTlnLDoqIrmga/lhazlkYo8YSBocmVmPWphdmFzY3JpcHQ6dm9pZCh3aW5kb3cub3BlbignTmV3c0Zvcm0uYXNweD9uZXdzSWQ9MjM0Jywn5pyA5paw5raI5oGvJywnbWVudWJhcj1ubyxzdGF0dXM9bm8sZGlyZWN0b3JpZXM9bm8sbWVudWJhcj1ubyxyZXNpemFibGU9bm8sdG9vbGJhcj1ubyxzY3JvbGxiYXJzPXllcyx0b3A9MjAwLGxlZnQ9MjAwLHdpZHRoPTU1MCxoZWlnaHQ9MzAwJykpPi4uLk1vcmU8L2E+ICDjgJAyMDE4LzExLzHmm7TmlrDjgJE8L3A+PHA+77yK57ac5ZCI6auU6IKy6aSo55CD6aGe5aC05Zyw6KiC5L2N6KaP5YmH6Kqq5piOPGEgaHJlZj1qYXZhc2NyaXB0OnZvaWQod2luZG93Lm9wZW4oJ05ld3NGb3JtLmFzcHg/bmV3c0lkPTIzMicsJ+acgOaWsOa2iOaBrycsJ21lbnViYXI9bm8sc3RhdHVzPW5vLGRpcmVjdG9yaWVzPW5vLG1lbnViYXI9bm8scmVzaXphYmxlPW5vLHRvb2xiYXI9bm8sc2Nyb2xsYmFycz15ZXMsdG9wPTIwMCxsZWZ0PTIwMCx3aWR0aD01NTAsaGVpZ2h0PTMwMCcpKT4uLi5Nb3JlPC9hPiAg44CQMjAxOC84LzMx5pu05paw44CRPC9wPjxwPu+8ikPpoZ7mnIPlk6HovqborYnjgIHkvb/nlKjloLTlnLDpoIjnn6U8YSBocmVmPWphdmFzY3JpcHQ6dm9pZCh3aW5kb3cub3BlbignTmV3c0Zvcm0uYXNweD9uZXdzSWQ9MjMwJywn5pyA5paw5raI5oGvJywnbWVudWJhcj1ubyxzdGF0dXM9bm8sZGlyZWN0b3JpZXM9bm8sbWVudWJhcj1ubyxyZXNpemFibGU9bm8sdG9vbGJhcj1ubyxzY3JvbGxiYXJzPXllcyx0b3A9MjAwLGxlZnQ9MjAwLHdpZHRoPTU1MCxoZWlnaHQ9MzAwJykpPi4uLk1vcmU8L2E+ICDjgJAyMDE4LzgvMTTmm7TmlrDjgJE8L3A+PHA+PC9tYXJxdWVlPmQCDQ9kFgICAQ9kFhICCA8PFgIfAAUHMTAxMjgzNWRkAgoPDxYCHwAFLee2nOWQiOmrlOiCsumkqOS4gOaoky0xRue+veeQg+WgtCAgICAgICAgICAgIGRkAgwPDxYCHwAFCeWKieW7uuWuj2RkAhoPDxYCHwAFBuWtuOeUn2RkAhwPEGQPFgJmAgEWAhAFBuePvumHkQUG54++6YeRZxAFCeaZguaVuOWIuAUG5pmC5pW4Z2RkAiAPDxYCHwAFCjIwMTgvMTEvMjdkZAIiDxBkDxYPZgIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4WDxAFBDg6MDAFAThnEAUEOTowMAUBOWcQBQUxMDowMAUCMTBnEAUFMTE6MDAFAjExZxAFBTEyOjAwBQIxMmcQBQUxMzowMAUCMTNnEAUFMTQ6MDAFAjE0ZxAFBTE1OjAwBQIxNWcQBQUxNjowMAUCMTZnEAUFMTc6MDAFAjE3ZxAFBTE4OjAwBQIxOGcQBQUxOTowMAUCMTlnEAUFMjA6MDAFAjIwZxAFBTIxOjAwBQIyMWcQBQUyMjowMAUCMjJnZGQCJA8QZA8WDmYCAQICAgMCBAIFAgYCBwIIAgkCCgILAgwCDRYOEAUEOTowMAUBOWcQBQUxMDowMAUCMTBnEAUFMTE6MDAFAjExZxAFBTEyOjAwBQIxMmcQBQUxMzowMAUCMTNnEAUFMTQ6MDAFAjE0ZxAFBTE1OjAwBQIxNWcQBQUxNjowMAUCMTZnEAUFMTc6MDAFAjE3ZxAFBTE4OjAwBQIxOGcQBQUxOTowMAUCMTlnEAUFMjA6MDAFAjIwZxAFBTIxOjAwBQIyMWcQBQUyMjowMAUCMjJnZGQCKg8PFgIfAAUsPEJSPiROVDEyMC/loLTmrKEo6Zui5bOw5pmC5q61MTA6MDDoh7MxMTowMClkZGRqWtdr9W7x6oMFLrvQ/QHpIrLMwQ==',
				'__VIEWSTATEGENERATOR': '2C8BDEE8',
				'__EVENTVALIDATION': '/wEWNQKW/KWVBgKenYa6CgKmgrS6BwKVmaKuDQLe9cW6DwLUnp3xAQKEhLO8BAKIv9+QCQKljKvkAQKpxZmADQKxqrPuAQK+qrPuAQKmqvPtAQKmqv/tAQKmqvvtAQKmqsftAQKmqsPtAQKmqs/tAQKmqsvtAQKmqtftAQKmqpPuAQKmqp/uAQKnqvPtAQKnqv/tAQKnqvvtAQK21/qxAwKhuNDfDwK5uJDcDwK5uJzcDwK5uJjcDwK5uKTcDwK5uKDcDwK5uKzcDwK5uKjcDwK5uLTcDwK5uPDfDwK5uPzfDwK4uJDcDwK4uJzcDwK4uJjcDwKSuJrlCwKT5+K1CAKG1qD0CQLj5c6uCgKEjN68DwKG7uXsBwLK/oeMDgKn6vbGBgKw7sSTBwL50tb0CQL50v6CCgLqqKuOCQKcjYHXDcTN1Ek8LP7ZjTwY2wCxhS2PIrZx',

				'ctl00$ContentPlaceHolder1$txtContactName': '',
				'ctl00$ContentPlaceHolder1$txtContactTel': '',
				'ctl00$ContentPlaceHolder1$txtFax': '',
				'ctl00$ContentPlaceHolder1$txtEmail': 'kw904@hotmail.com',
				'ctl00$ContentPlaceHolder1$DropLstPayMethod': '現金',
				'ctl00$ContentPlaceHolder1$txtpayHourNum': '',
				'ctl00$ContentPlaceHolder1$DropLstTimeStart': soup.find('input', id='ctl00_ContentPlaceHolder1_hidsTime')['value'],
				'ctl00$ContentPlaceHolder1$DropLstTimeEnd': soup.find('input', id='ctl00_ContentPlaceHolder1_hideTime')['value'],
				'ctl00$ContentPlaceHolder1$txtPlaceNum': '1',
				'ctl00$ContentPlaceHolder1$btnOrder': '送出預約',
				'ctl00$ContentPlaceHolder1$hidbookDate': soup.find('input', id='ctl00_ContentPlaceHolder1_hidbookDate')['value'],
				'ctl00$ContentPlaceHolder1$hidmemberId': soup.find('input', id='ctl00_ContentPlaceHolder1_hidmemberId')['value'],
				'ctl00$ContentPlaceHolder1$hidplaceSeq': soup.find('input', id='ctl00_ContentPlaceHolder1_hidplaceSeq')['value'],
				'ctl00$ContentPlaceHolder1$hidpayPrice': soup.find('input', id='ctl00_ContentPlaceHolder1_hidpayPrice')['value'],
				'ctl00$ContentPlaceHolder1$hidpeekCharge': soup.find('input', id='ctl00_ContentPlaceHolder1_hidpeekCharge')['value'],
				'ctl00$ContentPlaceHolder1$hidoffCharge': soup.find('input', id='ctl00_ContentPlaceHolder1_hidoffCharge')['value'],
				'ctl00$ContentPlaceHolder1$hidsTime': soup.find('input', id='ctl00_ContentPlaceHolder1_hidsTime')['value'],
				'ctl00$ContentPlaceHolder1$hideTime': soup.find('input', id='ctl00_ContentPlaceHolder1_hideTime')['value'],
				'ctl00$ContentPlaceHolder1$hidWeek': soup.find('input', id='ctl00_ContentPlaceHolder1_hidWeek')['value'],
				'ctl00$ContentPlaceHolder1$hiddateLst': soup.find('input', id='ctl00_ContentPlaceHolder1_hiddateLst')['value']}
		self.s.post(url, data=data)
		# Todo: Check if registered succesfully
