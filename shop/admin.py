from django.contrib import admin
from models import CoinToShop, ShopItem, ImageCoin

# Register your models here.
class ImageCoinAdmin(admin.StackedInline):
    model = ImageCoin


class CoinToShopAdmin(admin.StackedInline):
    model = CoinToShop

class ShopItemAdmin(admin.ModelAdmin):
    inlines = (
        CoinToShopAdmin,
        ImageCoinAdmin,
    )
    fields = ['user', 'quantity_lots', 'description']

admin.site.register(ShopItem, ShopItemAdmin)
#admin.site.register(CoinToShop, CoinToShopAdmin)
