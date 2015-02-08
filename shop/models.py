#-*- coding:utf-8 -*-
from django.db import models
from coins.models import Coins
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

# предложения продавцов
class ShopItem(models.Model):
    class Meta:
        db_table = 'ShopItems'
        verbose_name = 'Товар'
        verbose_name_plural='Товары'

    user = models.ForeignKey(User)
    quantity_lots = models.IntegerField()
    description = models.TextField()
    total_sum = models.FloatField(blank=True)

# товары в предложениях продавцов
class CoinToShop(models.Model):
    class Meta:
        db_table = 'CoinToShops'

    item = models.ForeignKey('ShopItem')
    coin = models.ForeignKey(Coins)
    quantity = models.IntegerField()
    price = models.FloatField()



# фото монет пользователей
class ImageCoin(models.Model):
    class Meta:
        db_table = 'ImageCoins'

    item = models.ForeignKey('ShopItem')
    image = models.FileField(upload_to='user_image')


# реквизиты продавца
class SellerPaymentDetal(models.Model):
    class Meta:
        db_table='SellerPaymentDetals'

    user = models.OneToOneField(User)
    number_card = models.IntegerField() # номер пластиковой карты
    first_name = models.TextField()
    last_name = models.TextField()
    middle_name = models.TextField()

    # окончание действия карты
    month_end = models.CharField(max_length=2, blank=True)
    year_end = models.IntegerField(max_length=4, blank=True, null=True)

    # номер телефона
    phone = models.IntegerField(max_length=10, unique=True, blank=True, null=True)

    # аккаунт в Яндекс.Деньги
    yandex_money = models.IntegerField(blank=True, null=True)


# оплата заказов
'''class Payment(models.Model):
    class Meta:
        db_table = 'Payments'

    or
'''
# покупки
class Order(models.Model):
    class Meta:
        db_table = 'Orders'

    items = models.ForeignKey('ShopItem') # купленный товар
    buyer = models.ForeignKey(User) # покупатель
    track_code = models.TextField() # отслеживание посылки
    date_buy = models.DateTimeField(default=timezone.now)

# адреса покупателей
class BuyerAddress(models.Model):
    class Meta:
        db_table = 'BuyerAddress'

    buyer = models.ForeignKey(User)
    city = models.TextField()
    zip_code = models.IntegerField(max_length=6)
    region = models.TextField()
    street = models.TextField()
    house = models.TextField()
    housing = models.TextField(blank=True) # корпус
    structure = models.TextField(blank=True) # строение
    flat = models.IntegerField(max_length=10000)