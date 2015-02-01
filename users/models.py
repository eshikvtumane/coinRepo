#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from coins.models import Coins, Mints, Countries, Series
from django.conf import settings
from os import path

# Create your models here.
class Profile(models.Model):
    class Meta:
        db_table = 'Profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'

    user = models.OneToOneField(User)
    first_name = models.CharField(verbose_name='Фамилия',max_length='100') # verbose_name=_(u'Фамилия'),
    last_name = models.CharField(verbose_name='Имя',max_length='100') # verbose_name=_(u'Имя'),
    middle_name = models.CharField(verbose_name='Отчество',null=True, blank=True, max_length='255') # verbose_name=_(u'Отчество'),
    avatar = models.ImageField(upload_to=settings.MEDIA_URL_AVATAR, default=path.join(settings.MEDIA_URL_AVATAR, 'default.jpg'), null=True, editable=True, verbose_name='Фото') #, verbose_name=_(u'Фото')

    def __unicode__(self):
        return unicode(self.user)

    def admin_image(self):
        return u'<img src="%s" style="width: 40%%; height:40%%"/>'%(path.join(settings.MEDIA_URL, self.avatar.url))

    def get_username(self):
        return self.user.username

    admin_image.short_description = u'Фото'
    admin_image.allow_tags = True


    get_username.short_description = 'Логин'
    get_username.admin_order_field = 'user__username'


# монеты пользователя
class UserCoins(models.Model):
    class Meta:
        db_table = 'UserCoins'
        #verbose_name = _(u'Монеты пользователя')
        #verbose_name_plural = _(u'Монеты пользователя')

    user = models.ForeignKey(User) # , verbose_name=_(u'Пользователь')
    coin_series = models.ForeignKey('UserSeries') # , verbose_name=_(u'Серия')
    coin = models.ForeignKey(Coins) # , verbose_name=_(u'Монета')

# выбранные страны
class UserCountries(models.Model):
    class Meta:
        db_table = 'UserCountries'
        #verbose_name = _(u'Выбранная страна')
        #verbose_name_plural = _(u'Выбранные страны')

    user = models.ForeignKey(User) # , verbose_name=_(u'Пользователь')
    country = models.ForeignKey(Countries) # , verbose_name=_(u'Страна')

class UserSeries(models.Model):
    class Meta:
        db_table = 'UserSeries'
        #verbose_name = _(u'Выбранная серия')
        #verbose_name_plural = _(u'Выбранные серии')

    user = models.ForeignKey(User) # , verbose_name=_(u'Пользователь')
    user_country = models.ForeignKey('UserCountries') # , verbose_name=_(u'Страна')
    user_series = models.ForeignKey(Series) # , verbose_name=_(u'Серия')

# описание монет
class UserCoinInfo(models.Model):
    class Meta:
        db_table = 'UserCoinsInfo'
        #verbose_name = _(u'Информация о монете')
        #verbose_name_plural = _(u'Информация о монете')

    user = models.ForeignKey(User)
    coin_user = models.ForeignKey('UserCoins') # , verbose_name=_(u'Монета')
    condition = models.ForeignKey('CoinsCondition') # , verbose_name=_(u'Состояние монеты')
    quantity = models.IntegerField() # verbose_name=_(u'Количество монет')
    mint = models.ForeignKey(Mints)
    defect_type = models.ForeignKey('Defects')
    note = models.CharField(max_length='255')

class CoinsPhoto(models.Model):
    class Meta:
        db_table='CoinsPhoto'
        #verbose_name=_(u'Фото монеты')
        #verbose_name_plural=_(u'Фотографии монет')

    photo = models.ImageField(upload_to='static/photo_coins_users')

# виды состояния монет
class CoinsCondition(models.Model):
    class Meta:
        db_table='CoinsCondition'
        #verbose_name=_(u'Состояние монеты')
        #verbose_name_plural=_(u'Состояние монет')

    condition_name = models.CharField(max_length='100') # verbose_name=_(u'Состояние монеты'),
    condition_abbr = models.CharField(max_length='3') # verbose_name=_(u'Аббревиатура'),
    condition_color = models.CharField(max_length='50') # verbose_name=_(u'Цвет'),

# виды браков у монет
class Defects(models.Model):
    class Meta:
        db_table='Defects'
        #verbose_name=_(u'Дефект монеты')
        #verbose_name_plural=_(u'Дефекты монеты')

    defect_name = models.CharField(max_length='50') # , verbose_name=_(u'Вид дефекта')



