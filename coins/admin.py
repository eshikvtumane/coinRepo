#-*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from coins.models import Countries,Series,Coins,CoinToMint,Metals,Mints, Prices
from django.utils.translation import gettext_lazy as _

class CountriesAdmin(admin.ModelAdmin):
    fields = ["country_name","country_flag"]
    list_display = ('country_name',)


class SeriesAdmin(admin.ModelAdmin):
    fields = ["series_name","country"]
    list_display = ["series_name", "get_country"]
    search_fields = ['series_name']
    list_filter = ('country__country_name',)

    def get_country(self, obj):
        return obj.country.country_name

    get_country.short_description = 'Страна'
    get_country.admin_order_field = 'country__country_name'

class CoinToMintInline(admin.StackedInline):
    model = CoinToMint


class CoinsAdmin(admin.ModelAdmin):
    inlines = [CoinToMintInline,]
    fields = ["country","series","coin_name","coin_metal","rate", 'denominal',"manufacture_date","coin_circulation",
             "coin_weight","coin_diameter","coin_thickness","painter","sculptor","coin_herd","item_number",
              "photo_obverse","photo_reverse","link_cbr", "chemistry", "quality"]
    list_display = ["coin_name", 'get_country',"rate",'denominal',"get_series", "get_quality", 'admin_image']

    search_fields = ('coin_name',)
    list_filter = ('rate', 'denominal')
    #list_filter = ("coin_name",)

    def get_series(self, obj):
        return '%s'%(obj.series.series_name)
    def get_country(self, obj):
        return '%s'%(obj.country.country_name)
    def get_quality(self, obj):
        return '%s'%(obj.quality.quality_coinage)

    get_series.short_description = 'Серия монет'
    get_series.admin_order_field = 'series__series_name'

    get_country.short_description = 'Страна'
    get_country.admin_order_field = 'country__country_name'

    get_quality.short_description = 'Качество'
    get_quality.admin_order_filter = 'quality__quality_coinage'

    '''def __init__(self, *args, **kwargs):
        super(CoinsAdmin, self).__init__(*args, **kwargs)'''


'''class CoinToMintAdmin(forms.ModelAdmin):
    fields = ["coin","mint"]
    list_display = ['get_coin', 'get_mint']
    search_fields = ('coin_id__coins__id', 'mint',)

    def get_coin(self, obj):
        return obj.coin.coin_name
    def get_mint(self, obj):
        return obj.mint.mint_name

    get_coin.short_description = _('Монета')
    get_coin.admin_order_filter = 'coin__coin_name'
    get_mint.short_description = _('Монетный двор')
    get_mint.admin_order_filter = 'mint__mint_name'
'''

class MetalsAdmin(admin.ModelAdmin):
    fields = ["metal_description"]

class MintsAdmin(admin.ModelAdmin):
    fields = ["country","mint_name","mint_abbreviation"]
#class DenominalsAdmin(admin.ModelAdmin):
 #   fields = ["denominal_name","denominal_country"]

class PricesAdmin(admin.ModelAdmin):
    fields = ['coin', 'price', 'link', 'date']


admin.site.register(Countries,CountriesAdmin)
admin.site.register(Series,SeriesAdmin)
admin.site.register(Coins,CoinsAdmin)
#admin.site.register(CoinToMint,CoinToMintAdmin)
admin.site.register(Metals,MetalsAdmin)
admin.site.register(Mints,MintsAdmin)
admin.site.register(Prices, PricesAdmin)
#admin.site.register(Denominals,DenominalsAdmin)
