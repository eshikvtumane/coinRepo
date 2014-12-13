from django.db import models
from coins.models import Coins
from django.contrib.auth.models import User

class CoinToUser(models.Model):
    class Meta:
        db_table = "CoinToUser"
    user = models.ForeignKey(User)
    coin = models.ForeignKey(Coins)