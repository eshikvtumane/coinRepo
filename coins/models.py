#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.


class Countries(models.Model):
	'''Table for countries'''
	class Meta:
		db_table = 'Countries' # table name in DB
		verbose_name = _(u'Страна')
		verbose_name_plural = _(u'Страны')

	country_name = models.CharField(max_length='200', verbose_name=_(u'Название страны'))
	country_flag = models.ImageField(upload_to='/static/flag', blank=True, verbose_name=_(u'Флаг страны')) # Image flag for country

	def __unicode__(self):
		return self.country_name


# http://tinyurl.com/pbbzjv7 - link to Wikipedia, paragraph 3.
class Series(models.Model):
	'''Table with coins series name '''
	class Meta:
		db_table = 'Series' # name table in DB
		verbose_name = _(u'Серия монеты')
		verbose_name_plural = _(u'Серия монет')

	country = models.ForeignKey('Countries')
	series_name = models.CharField(max_length='255')

	def __unicode__(self):
		return self.series_name

class Metals(models.Model):
	class Meta():
		db_table = 'Metals'
		verbose_name = _(u'Металл')
		verbose_name_plural = _(u'Металлы')

	metal_description = models.CharField(max_length='255', verbose_name=_(u'Название металла'))

	def __unicode__(self):
		return self.metal_description


class Mints(models.Model):
	class Meta:
		db_table = 'Mints'
		verbose_name = _(u'Монетный двор')
		verbose_name_plural = _(u'Монетные дворы') #  отображение имени модели во множественном числе

	country = models.ForeignKey('Countries', verbose_name=_(u'Страна'))
	mint_name = models.CharField(max_length='200', verbose_name=_(u'Название монетного двора'))
	mint_abbreviation = models.CharField(max_length=10, verbose_name=_(u'Аббревиатура'))

	def __unicode__(self):
		return self.mint_abbreviation


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
		verbose_name_plural = _(u'Качество монет')

	quality_coinage = models.CharField(max_length='30')
	quality_abbr = models.CharField(max_length='10', blank=True)
	quality_description = models.CharField(max_length='255')

	def __unicode__(self):
		return self.quality_coinage


class Coins(models.Model):
	class Meta:
		db_table = 'Coins' # name table in DB
		verbose_name = _(u'Монеты')
		verbose_name_plural = _(u'Монеты')

	country = models.ForeignKey('Countries',verbose_name=_(u'Страна'))
	series = models.ForeignKey('Series',verbose_name=_(u'Серия'))
	coin_metal = models.ForeignKey('Metals',verbose_name=_(u'Металл'))
	quality = models.ForeignKey('Qualities', verbose_name=_(u'Качество'))

	coin_name = models.CharField(max_length='255', verbose_name=_(u'Название монеты'))
	link_cbr = models.URLField(verbose_name=_(u'Сайт банка')) # link on description coin on site Central Bank of Russia
	description_observe = models.CharField(max_length='255', verbose_name='Описание аверса')
	description_reverse = models.CharField(max_length='255', verbose_name='Описание реверса')
	painter = models.CharField(max_length='255', verbose_name='Художник(и)')
	sculptor = models.CharField(max_length='255', verbose_name='Скульптор(ы)')
	coin_herd = models.CharField(max_length='255', blank=True, verbose_name='Описание гурта') # edge of a coin http://tinyurl.com/m56ms6y
	photo_obverse = models.ImageField(upload_to='/static/coins', verbose_name='Фото аверса')
	photo_reverse = models.ImageField(upload_to='/static/coins', verbose_name='Фото реверса')

	rate = models.IntegerField(verbose_name='Номинал') #coin rating
	denominal = models.CharField(max_length='255', verbose_name='Валюта')
	#denominal_name = models.ForeignKey('Denominals') #currency
	coin_weight = models.FloatField(blank=True, verbose_name='Вес')
	chemistry = models.FloatField(blank=True, verbose_name='Содержание химически чистого металла')
	coin_diameter = models.FloatField(blank=True, verbose_name='Диаметр')
	coin_thickness = models.FloatField(blank=True, verbose_name='Толщина')
	coin_circulation = models.BigIntegerField(verbose_name='Тираж')
	manufacture_date = models.DateField(verbose_name='Дата выпуска')
	item_number = models.CharField(max_length=9, verbose_name='Каталожный номер') # http://tinyurl.com/kbh5fly

	'''def __unicode__(self):
		return'''

class CoinToMint(models.Model):
	class Meta:
		db_table = 'CoinToMint'
		verbose_name = _(u"Монеты-Монетный двор")
		verbose_name_plural = _(u"Монеты-Монетный двор")

	coin = models.ForeignKey('Coins', verbose_name=_(u'Монета'))
	mint = models.ForeignKey('Mints', verbose_name=_(u'Монетный двор'))

	def __unicode__(self):
		return self.coin.coin_name



