import requests
# from bs4 import BeautifulSoup
import re
import os
import datetime


class SportCenter():
	def __init__(self):
		self.s = requests.session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
		self.root_url = 'http://info2.ntu.edu.tw'
		self.username = str()
		self.password = str()
		self.is_login = False
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
					a = re.search('''14dot1b.gif'.*?/> ?\((\d{,3})\)<''', data[i]) #o
					b = re.search('''actn010_2.gif'.*?/> ?\((\d{,3})\)<''', data[i]) #v
					c = re.search('''#696969">(.*?)<''', data[i]) #現場訂位

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

