import requests
import os

os.chdir(os.getcwd()+ '\\TestSet')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
		x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
url = 'https://info2.ntu.edu.tw/facilities/ValidateCode.aspx?ImgID=Login'


for i in range(2483,10000):
    img = requests.get(url=url, headers=headers)
    
    with open('{}.png'.format(i), 'wb') as f:
        f.write(img.content)
