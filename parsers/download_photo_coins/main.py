import xlrd
import urllib
import progressbar
import time
from multiprocessing import Pool

def imageDownload(x):
	r = x.split('/')
	urllib.urlretrieve(x, r[6])
	print x + ' - Ok'

if __name__ == '__main__':
	rb = xlrd.open_workbook('coins.xls', formatting_info=True)
	sheet = rb.sheet_by_index(0)
	rows = sheet.nrows
	result1 = [sheet.row_values(rownum)[11] for rownum in xrange(rows)]
	result2 = [sheet.row_values(rownum)[12] for rownum in xrange(rows)]

	result = result1[1:] + result2[1:]
	#bar = progressbar.ProgressBar(maxval=len(result)).start()
	pool = Pool(processes=4)
	pool.map(imageDownload, result)
	print 'Complete'
	'''for x in result:
		try:
			bar.update(counter)
			r = x.split('/')
			urllib.urlretrieve(x, r[6])
		except:
			print x'''


