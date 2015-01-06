import datetime
import urllib2
from bs4 import BeautifulSoup as BS
import re

class ParcePrice():
	def __init__(self):
		self.stop_list = ()

	def get_price(self, obj):
		date = datetime.date.today()
		results = ()
		link = 'http://molotok.ru/listing/listing.php?category=48393&p='
		link_end = '&search_scope=category-48393&string=%s+%s+%s' % (obj[2], obj[3], obj[1].replace(' ', '+'))

		count_page = 1
		buf_result = []
		while(True):
			res = []
			while(True):
				try:
					res = self.parse_prices(link + str(count_page) + link_end)
					break
				except:
					print 'Error connect. Retry ...'
			if res == []:
				break
			if count_page > 5:
				break
			buf_result += res
			count_page += 1

		if buf_result != []:
			results = (obj[0], self.get_median(buf_result), '%s1%s'%(link, link_end), date, )
			return results
		
		return False

	def parse_prices(self, link):
		response = urllib2.urlopen(link)
		html = response.read()
		#print link
		page = BS(html)
		prices = page.findAll('span', {'class':'bid dist', 'class':'buy-now dist'})
		
		array_prices = []
		if prices:
			for obj in prices:
				price = re.findall('\d+.\d+', obj.get_text())
				arr_price = [ float(p.replace(',', '.').replace(' ', '')) for p in price ]
				array_prices += arr_price
		return array_prices

	def get_median(self, arr):
		arr.sort()
		length_arr = len(arr)

		if length_arr % 2 == 0:
			return (arr[(length_arr / 2) - 1] + arr[(length_arr / 2)]) / 2
		return arr[int(length_arr / 2)]