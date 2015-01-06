import sqlite3 as lite
from MolotokParce import *
import multiprocessing as mp


result = []

def connect_db():
	try:
		con = lite.connect('/home/eshik/projects/coins/coinRepo/db.sqlite3')
		con.text_factory = str
		return con
	except lite.Error, e:
		print 'Error: %s'%e.args[0]

def connect_close(con):
	con.close()

def get_coins(con):
	sql = 'SELECT id, coin_name, rate, denominal FROM Coins'

	cur = con.cursor()
	cur.execute(sql)
	select = cur.fetchall()
	#for obj in select:
		#print obj
	return select

def get_price(obj):
	price = ParcePrice()
	price_obj = price.get_price(obj)
	print obj[1]
	return price_obj
		




def insert_data(con, data):
	sql_insert = 'INSERT INTO Price(coin_id, price, link, date) VALUES(?,?,?,?)'
	con.executemany(sql_insert, data)
	con.commit()

if __name__ == '__main__':
	print 'Connect DB ...'
	con = connect_db()
	print 'Get coins ...'
	coins = get_coins(con)
	print 'Get prices ...'
	pool = mp.Pool(processes = 20)

	result = pool.map(get_price, coins)

	'''result = []
	for obj in coins[:5]:
		p = mp.Process(target=get_price, args = (obj,))
		result.append(p)
		p.start()'''

	while False in result:
		result.remove(False)

	print 'Insert data'
	insert_data(con, result)
	print 'Connect close ...'
	connect_close(con)





