#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Countries(models.Model):
	'''Table for store name countries'''
	class Meta:
		db_table = 'Countries' # name table in DB

	#id = models.AutoField(primary_key=True) # id
	country_name = models.CharField(max_length='200')
	country_flag = models.ImageField(upload_to='/static/flag', blank=True) # Image flag for country


# http://tinyurl.com/pbbzjv7 - link to Wikipedia, paragraph 3.
class Series(models.Model):
	'''Table with names series coins '''
	class Meta:
		db_table = 'Series' # name table in DB

	#series = models.AutoField(primary_key=True) # id
	country = models.ForeignKey('Countries')
	series_name = models.CharField(max_length='255')

class Metals(models.Model):
	class Meta():
		db_table = 'Metals'

	#metal = models.AutoField(primary_key=True)
	metal_description = models.CharField(max_length='255')


class Mints(models.Model):
	class Meta:
		db_table = 'Mints'

	#mint = models.AutoField(primary_key=True)
	country = models.ForeignKey('Countries')
	mint_name = models.CharField(max_length='200')
	mint_abbreviation = models.CharField(max_length=10)


#class Denominals(models.Model):
#	''' "ruble, dollar" for example '''
#	class Meta:
#		db_table = 'Denominals'
#
#	denominal_name = models.CharField(max_length='50')
#	denominal_country = models.ForeignKey('Countries')

# Качество чеканки монет
class Qualities(models.Model):
	class Meta:
		db_table = 'Qualities'
	quality_coinage = models.CharField(max_length='30')
	quality_abbr = models.CharField(max_length='10', blank=True)
	quality_description = models.CharField(max_length='255')


class Coins(models.Model):
	class Meta:
		db_table = 'Coins' # name table in DB

	#coin = models.AutoField(primary_key=True) # id
	country = models.ForeignKey('Countries')
	series = models.ForeignKey('Series')
	coin_metal = models.ForeignKey('Metals')
	quality = models.ForeignKey('Qualities')

	coin_name = models.CharField(max_length='255')
	link_cbr = models.URLField() # link on description coin on site Central Bank of Russia
	description_observe = models.CharField(max_length='255')
	description_reverse = models.CharField(max_length='255')
	painter = models.CharField(max_length='255')
	sculptor = models.CharField(max_length='255')
	coin_herd = models.CharField(max_length='255', blank=True) # edge of a coin http://tinyurl.com/m56ms6y
	photo_obverse = models.ImageField(upload_to='/static/coins')
	photo_reverse = models.ImageField(upload_to='/static/coins')

	rate = models.IntegerField() #coin rating
	denominal = models.CharField(max_length='255')
	#denominal_name = models.ForeignKey('Denominals') #currency
	coin_weight = models.FloatField(blank=True)
	chemistry = models.FloatField(blank=True)
	coin_diameter = models.FloatField(blank=True)
	coin_thickness = models.FloatField(blank=True)
	coin_circulation = models.BigIntegerField()
	manufacture_date = models.DateField()
	item_number = models.CharField(max_length=9) # http://tinyurl.com/kbh5fly


class CoinToMint(models.Model):
	class Meta:
		db_table = 'CoinToMint'

	#cmd = models.AutoField(primary_key=True)
	coin = models.ForeignKey('Coins')
	mint = models.ForeignKey('Mints')



