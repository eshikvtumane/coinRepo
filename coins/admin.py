from django.contrib import admin
from coins.models import Countries,Series,Coins,CoinToMint,Metals,Mints,Denominals

class CountriesAdmin(admin.ModelAdmin):
    fields = ["country_name","country_flag"]


class SeriesAdmin(admin.ModelAdmin):
    fields = ["series_name","country"]

class CoinsAdmin(admin.ModelAdmin):
    fields = ["country","series","coin_metal","rate","denominal_name","manufacture_date","coin_circulation",
             "coin_weight","coin_diameter","coin_thickness","painter","sculptor","coin_herd","description","item_number",
              "photo_obverse","photo_reverse","link_cbr"]

class CoinToMintAdmin(admin.ModelAdmin):
    fields = ["coin","mint"]

class MetalsAdmin(admin.ModelAdmin):
    fields = ["metal_description"]

class MintsAdmin(admin.ModelAdmin):
    fields = ["country","mint_name","mint_abbreviation"]
class DenominalsAdmin(admin.ModelAdmin):
    fields = ["denominal_name","denominal_country"]

admin.site.register(Countries,CountriesAdmin)
admin.site.register(Series,SeriesAdmin)
admin.site.register(Coins,CoinsAdmin)
admin.site.register(CoinToMint,CoinToMintAdmin)
admin.site.register(Metals,MetalsAdmin)
admin.site.register(Mints,MintsAdmin)
admin.site.register(Denominals,DenominalsAdmin)
