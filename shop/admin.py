from django.contrib import admin
from models import CoinToShop, ShopItem

# Register your models here.
class CoinToShopAdmin(admin.StackedInline):
    model = CoinToShop

class ShopItemAdmin(admin.ModelAdmin):
    inlines = (
        CoinToShopAdmin,
    )
    fields = ['user', 'quantity_lots', 'description']

admin.site.register(ShopItem, ShopItemAdmin)
#admin.site.register(CoinToShop, CoinToShopAdmin)
