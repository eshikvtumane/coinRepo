#-*- coding:utf-8 -*-
import xlrd
import sqlite3 as lite
import progressbar

def connectDB():
	try:
		con = lite.connect('/home/eshik/coins_project/project/coins_site/db.sqlite3')
		return con
	except lite.Error, e:
		print 'Error: %s'%e.args[0]

def closeConnect(con):
	con.close()

def insertCountries(con):
	countries = u'Российская Федерация'
	cur = con.cursor()
	cur.execute('INSERT INTO Countries(country_name, country_flag) VALUES (?,?)', (countries,'/static/flags/ru.jpg',))


	'''for country in countries:
		sql = "SELECT country_name from Countries WHERE country_name=%s" % (country,)
		con.execute(sql)
		con.commit()

		result = con.fetchone()
		if len(result) > 0:
			country_id.append[result[0]]
		else:
			con.execute('INSERT INTO Countries(country_name) VALUES (?)', (country,))
			con.commit()
			country_id.append[con.insert_id()]'''

	return int(cur.lastrowid)

def deleteDuplicate(series, countries):
	result = []
	res = []
	for s in series:
		if s not in result:
			#res.append[(countries,) + (s,)]
			result.append(s)
	return result, res

def insertSeries(con, countries, series):
	
	result, rest = deleteDuplicate(series, countries)

	'''sql_select = 'SELECT series_name FROM Series'
	con.execute(sql_select)
	con.commit()
	select_result = con.fetchone()'''

	sql_insert = ''
	for res in result:
		con.execute('INSERT INTO Series(country_id, series_name) VALUES (?,?)', (countries, res,))
		con.commit()
			

def insertMints(con,countries):
	mints = [
		(u'Московский монетный двор', u'ММД', countries,),
		(u'Санкт-Петербургский монетный двор', u'СПМД', countries,),
		(u'Ленинградский монетный двор', u'ЛМД', countries,)
	]

	sql = 'INSERT INTO Mints(mint_name, mint_abbreviation, country_id) VALUES (?,?,?)'
	con.executemany(sql, mints)
	con.commit()

def insertMetals(con,metals):
	result = []
	res = []
	for s in metals:
		if s not in result:
			result.append(s)

	for i in result:
		con.execute('INSERT INTO Metals(metal_description) VALUES (?)', (i,))
		con.commit()

def insertQuanties(con):
	quanties = [
		('uncirculated', 'UC', u'Монеты обычного качества'),
		('brilliant uncirculated','BA',u'Монеты улучшенного качества'),
		('proof','',u'Монеты высшего качества'),
		('proof-like','',u'Подобные пруфу. Этот термин появился для обозначения качества монет, которые внешне похожи на пруф, однако монетный двор не гарантирует, что при их изготовлении технология «пруф» была соблюдена полностью.'),
		('reverse frosted','',u'На поверхности монеты формируется шелковисто-матовое поле, а рельеф, напротив, зеркально-блестящий')
	]

	sql = 'INSERT INTO Qualities(quality_coinage,quality_abbr,quality_description) VALUES (?,?,?)'
	con.executemany(sql, quanties)
	con.commit()

def insertCoins(con, countries, wb):
	select_quanties = 'SELECT id, quality_coinage FROM Qualities'
	select_mints = 'SELECT id FROM Mints'
	select_series = 'SELECT id, series_name FROM Series WHERE country_id=%s'%countries
	select_metals = 'SELECT id, metal_description FROM Metals'

	cur = con.cursor()
	cur.execute(select_quanties)
	quanties = cur.fetchall()
	cur.execute(select_mints)
	mints = cur.fetchall()
	cur.execute(select_series)
	series = cur.fetchall()
	cur.execute(select_metals)
	metals = cur.fetchall()

	quanties_rus = {
		u'АЦ':'uncirculated', 
		u'пруф':'proof', 
		u'пруф-лайк':'proof-like', 
		u'БА':'brilliant uncirculated'
	}

	bar = progressbar.ProgressBar(maxval=rows-1).start()
	for i in xrange(1, rows):
		bar.update(i)
		query = (countries,)
		for s in series:
			if s[1] == ws.row_values(i)[2]:
				query += (s[0],)
				break
		for m in metals:
			if m[1] == ws.row_values(i)[16]:
				query += (m[0],)
				break

		qua = quanties_rus[ws.row_values(i)[15]]
		for q in quanties:
			if q[1] == qua:
				query += (q[0],)
				break

		query += (ws.row_values(i)[0],) # name
		query += (ws.row_values(i)[1],) # link
		query += (ws.row_values(i)[3],) # desc1
		query += (ws.row_values(i)[4],) # desc2
		query += (ws.row_values(i)[5],) # painter
		query += (ws.row_values(i)[6],) # sculptor
		query += (ws.row_values(i)[10],) # herd
		query += ('/static/coins/%s.jpg'%ws.row_values(i)[23],) # photo1
		query += ('/static/coins/%sr.jpg'%ws.row_values(i)[23],) # photo2
		
		query += (ws.row_values(i)[13],) # rate
		query += (ws.row_values(i)[14],) # denomenal
		query += (ws.row_values(i)[17],) # weigth
		query += (ws.row_values(i)[18],) # chemistry
		query += (ws.row_values(i)[19],) # diametr
		query += (ws.row_values(i)[20],) # thickness
		query += (ws.row_values(i)[21],) # circulation
		query += (ws.row_values(i)[22],) # date
		query += (ws.row_values(i)[23],) # item_number

		cur.execute('INSERT INTO Coins(country_id, series_id, coin_metal_id, quality_id, coin_name,link_cbr,description_observe,description_reverse,painter,sculptor,coin_herd,photo_obverse,photo_reverse,rate,denominal,coin_weight,chemistry,coin_diameter,coin_thickness,coin_circulation,manufacture_date,item_number) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',query)


		coins_id = int(cur.lastrowid)

		mint = []
		if ws.row_values(i)[7] == u'Да':
			mint.append((coins_id, mints[0][0],))
		if ws.row_values(i)[8] == u'Да':
			mint.append((coins_id, mints[1][0],))
		if ws.row_values(i)[9] == u'Да':
			mint.append((coins_id, mints[2][0],))

		sql = 'INSERT INTO CoinToMint(coin_id, mint_id) VALUES (?,?)'
		con.executemany(sql, mint)
		con.commit()
	bar.finish()

if __name__ == '__main__':
	wb = xlrd.open_workbook('coins.xls', formatting_info=True)
	ws = wb.sheet_by_index(0)
	rows = ws.nrows
	series = []
	metals = []
	for i in xrange(1, rows):
		s = ws.row_values(i)[2]
		metals.append(ws.row_values(i)[16])
		series.append(s)
		'''if s.strip() == '':
			series.append(u'Без серии')
		else:
			series.append(s)'''


	print 'Connect to DB ...'
	con = connectDB()
	print ' \r OK'
	print 'Delete info on table ...'
	tbl = ['Countries', 'Mints', 'Series', 'Metals', 'Coins', 'CoinToMint', 'Qualities']
	for t in tbl:
		con.execute('DELETE FROM %s'%(t,))
	print ' \r OK'
	print 'Add Countries ...'
	countries = insertCountries(con)
	print ' \r OK'
	print 'Add Series ...'
	insertSeries(con, countries, series)
	print ' \r OK'
	print 'Add Mints ...'
	insertMints(con,countries)
	print ' \r OK'
	print 'Add Metals ...'
	insertMetals(con, metals)
	print ' \r OK'
	print 'Add Qualities ...'
	insertQuanties(con)
	print ' \r OK'
	print 'Add Coins ...'
	insertCoins(con, countries, wb)
	print ' \r OK'
	print 'Complete.'
	closeConnect(con)

