from django.db import models

# Create your models here.


class Countries(models.Model):
	'''Table for store name countries'''
	class Meta:
		db_table = 'Countries' # name table in DB

	#id = models.AutoField(primary_key=True) # id
	country_name = models.CharField(max_length=200)
	country_flag = models.ImageField() # Image flag for country 


# http://tinyurl.com/pbbzjv7 - link to Wikipedia, paragraph 3.
class Series(models.Model):
	'''Table with names series coins '''
	class Meta:
		db_table = 'Series' # name table in DB

	#series = models.AutoField(primary_key=True) # id
	country = models.ForeignKey('Countries')
	series_name = models.CharField(max_length=100000)

class Metals(models.Model):
	class Meta():
		db_table = 'Metals'

	#metal = models.AutoField(primary_key=True)
	metal_description = models.CharField(max_length='10000')


class Mints(models.Model):
	class Meta:
		db_table = 'Mints'

	#mint = models.AutoField(primary_key=True)
	country = models.ForeignKey('Countries')
	mint_name = models.CharField(max_length='200')
	mint_abbreviation = models.CharField(max_length=10)


class Denominals(models.Model):
	''' "ruble, dollar" for example ''' 
	class Meta:
		db_table = 'Denominals'

	denominal_name = models.CharField(max_length='50')
	denominal_country = models.ForeignKey('Countries')


class Coins(models.Model):
	class Meta:
		db_table = 'Coins' # name table in DB

	#coin = models.AutoField(primary_key=True) # id
	country = models.ForeignKey('Countries')
	series = models.ForeignKey('Series')
	coin_metal = models.ForeignKey('Metals')

	rate = models.IntegerField() #coin rating
	denominal_name = models.ForeignKey('Denominals') #currency

	manufacture_date = models.DateField()
	coin_circulation = models.BigIntegerField()
	coin_weight = models.FloatField()
	coin_diameter = models.FloatField()
	coin_thickness = models.FloatField()
	painter = models.CharField(max_length='100')
	sculptor = models.CharField(max_length='100')
	coin_herd = models.CharField(max_length='10000') # edge of a coin http://tinyurl.com/m56ms6y
	description = models.CharField(max_length='1000000')
	item_number = models.CharField(max_length=9) # http://tinyurl.com/kbh5fly
	photo_obverse = models.ImageField()
	photo_reverse = models.ImageField()
	link_cbr = models.URLField() # link on description coin on site Central Bank of Russia




class  CoinToMint(models.Model):
	class Meta:
		db_table = 'CoinToMint'

	#cmd = models.AutoField(primary_key=True)
	coin = models.ForeignKey('Coins')
	mint = models.ForeignKey('Mints')



