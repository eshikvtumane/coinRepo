#-*- coding:utf-8 -*-
from django.contrib import admin
from users.models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import Profile, UserCountries, UserSeries, UserCoins, Defects
from django.conf import settings
from os import path

# Register your models here.

#http://stackoverflow.com/questions/5498152/how-to-create-own-extended-user_image-form
class ProfileInline(admin.StackedInline):
    model = Profile

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'f_name', 'l_name', 'm_name','avatar')
    inlines = [ProfileInline,]
    search_fields = ('username', 'email',)

    def avatar(self, obj):
        try:
            href = u'<img src="/media/%s" style="width: 40%%; height:40%%"/>'
            avatar = href % obj.profile.avatar
            return avatar
        except:
            return ''

    def f_name(self, obj):
        try:
            name = obj.profile.first_name
            return name
        except:
            return ''

    def l_name(self, obj):
        try:
            name = obj.profile.last_name
            return name
        except:
            return ''

    def m_name(self, obj):
        try:
            name = obj.profile.middle_name
            return name
        except:
            return ''

    avatar.short_description = 'Фото'
    avatar.allow_tags = True
    f_name.short_description = 'Фамилия'
    l_name.short_description = 'Имя'
    m_name.short_description = 'Отчество'


class UserCountriesAdmin(admin.ModelAdmin):
    fields = ['country', 'user_image']

class UserSeriesAdmin(admin.ModelAdmin):
    fields = ['user_image', 'user_country', 'user_series']

class UserCoinsAdmin(admin.ModelAdmin):
    fields = []

class DefectsAdmin(admin.ModelAdmin):
    fields = ['defect_name']

admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(UserCountries, UserCountriesAdmin)
admin.site.register(UserSeries, UserSeriesAdmin)
admin.site.register(UserCoins, UserCoinsAdmin)
admin.site.register(Defects, DefectsAdmin)