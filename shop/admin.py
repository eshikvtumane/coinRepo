from django.contrib import admin
from models import CoinToShop, ShopItem, ImageCoin

# Register your models here.edInline):
class ImageCoinAdmin(admin.StackedInline):
    model = ImageCoin

class CoinToShopAdmin(admin.StackedInline):
    model = CoinToShop

class ShopItemAdmin(admin.ModelAdmin):
    inlines = (
        CoinToShopAdmin,
        ImageCoinAdmin,
    )

admin.site.register(ShopItem, ShopItemAdmin)
#admin.site.register(CoinToShop, CoinToShopAdmin)
