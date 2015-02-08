#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View, TemplateView
from django.template import RequestContext,Template

from django.core.context_processors import csrf
from django.core import serializers
import json

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from models import Countries, Series, Qualities, Metals, Coins, Mints, CoinToMint, Prices, WishListModel
from users.models import UserCoins, UserCountries, UserSeries

from django.db.models import Q # http://proft.me/2011/01/22/polnotekstovyj-poisk-v-django/
import operator
#from django_ajax.mixin import AJAXMixin # https://github.com/yceruto/django-ajax
#import django_ajax.shortcuts

#http://django-haystack.readthedocs.org/en/latest/tutorial.html
from haystack.query import SearchQuerySet
import json

# charts
from chartit import DataPool, Chart
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required

#
# Create your views here.

'''def ajax(request):
     country = request.GET["country"]
     mints = list(Mints.objects.filter(country_id=country))
     print mints
     c = RequestContext(request,{'result':serializers.serialize("json",mints)})
     t = Template("{{result|safe}}")
     response = HttpResponse(t.render(c),content_type='application/json')
     return response'''


class CatalogView(View):
    def get(self, request):
        countries = Countries.objects.all()
        args = {}
        args.update(csrf(request))
        args = RequestContext(request, {'countries':countries})
        return render_to_response('catalog/catalog.html', args)

class CoinsView(View):

    def get(self, request, country_id):
        template_name = 'catalog/coins.html'
        series = Series.objects.filter(country_id=country_id)
        qualities = Qualities.objects.all()
        metals = Metals.objects.all()
        coins = Coins.objects.order_by('?')[0:15] # select random coins objects
        args = RequestContext(request, {'series':series, 'qualities':qualities, 'metals':metals, 'coins':coins, 'country': country_id})
        return render_to_response(template_name, args)


class SearchView(View):
    template_name = 'catalog/catalog.html'
    model = Series

# full text search name coins
    def get(self, request):
        coins = SearchQuerySet().autocomplete(content_auto=request.GET['search_name'])
        json = serializers.serialize('json', [coin.object for coin in coins], fields=('coin_name'))
        return HttpResponse(json, content_type='application/json')

# search coins
    def post(self, request):
        if self.request.is_ajax():
            series = request.POST['series']
            name = request.POST.get('name')
            number = request.POST['item_number']
            metals = request.POST['metals']
            qualities = request.POST['qualities']
            number_page = request.POST['page']
            first_load = request.POST['first_load']

            country = request.POST['country']

            criterions = []

            if not number:
                if country != ''.strip():
                    criterions.append(Q(country_id=int(country)),)
                if series != '':
                    criterions.append(Q(series_id=series),)
                if name != '':
                    criterions.append(Q(coin_name__contains=name),)
                if qualities != '':
                    criterions.append(Q(quality_id=qualities),)
                if metals != '':
                    criterions.append(Q(coin_metal_id=metals))
            else:
                criterions.append(Q(item_number = number))

            page_size = 15
            total_pages, obj = False, False
            if first_load == 'True':
                total_pages, obj = self.firstLoad(criterions, page_size)
            else:
                total_pages, obj = self.pageLoad(criterions, number_page, page_size)

            data = serializers.serialize('json', obj, fields=('id', 'coin_name', 'photo_reverse', 'rate', 'denominal'))
            result = json.dumps([total_pages,data])

            return HttpResponse(result, content_type='application/json')

    # function work at first search coins
    def firstLoad(self, criterions, page_size):
        obj = Coins.objects.filter(reduce(operator.and_,criterions)) #item_number=number

        count_objs = obj.count()
        total_pages = (count_objs + page_size - 1) / page_size

        return total_pages, obj[0:page_size]

    # function work at transition page to page
    def pageLoad(self, criterions, page, page_size):
        filter_end = int(page_size) * int(page)
        filter_start = int(filter_end) - int(page_size)

        obj = Coins.objects.filter(reduce(operator.and_,criterions))[filter_start:filter_end] #item_number=number
        total_pages = 0

        return total_pages, obj

class CoinSelectView(View):
    def get(self, request, country_id, coin_id):
        rend = self.get_coin_info(request, country_id, coin_id)
        return rend

    def post(self, request, country_id, series_id, coin_id):
        user = request.user
        country = Countries.objects.get(pk = country_id)
        series = Series.objects.get(pk = series_id)
        coin = Coins.objects.get(pk = coin_id)

        uc, created = UserCountries.objects.get_or_create(user = user, country = country)
        us, created = UserSeries.objects.get_or_create(user = user, user_country = uc, user_series = series)
        u_coin = UserCoins.objects.get_or_create(user = user, coin_series = us, coin = coin)

        rend = self.get_coin_info(request, country_id, coin_id)
        return rend

# formind chart
    def draw_chart(self, coin_obj):
        #Step 1: Create a DataPool with the data we want to retrieve.
        data = DataPool(
            series=
            [{
                'options': {
                  'source': Prices.objects.filter(coin = coin_obj).values('price', 'date')
                },
                'terms':[
                    'date',
                    'price'
                ]}
            ])
        #Step 2: Create the Chart object
        cht = Chart(
            datasource = data,
            series_options =
                [{
                    'options': {
                        'type': 'line',
                        'stacking': False},
                    'terms':{
                        'date':[
                            'price'
                        ]
                    }
                }],
            chart_options=
            {
                'title':{
                    'text':u'Курс Монета/руб'
                },
                'xAxis':{
                    'title':{
                        'text': u'Дата'
                    }
                },
                'yAxis':{
                  'title':{
                      'text': u'Цена'
                  }
                },
                'legend': {
                    'enabled': False
                }
            }
        )

        return cht

    def get_coin_info(self, request, country_id, coin_id):
        template = 'catalog/coin_descr.html'
        description = Coins.objects.filter(id=coin_id, country=country_id).values('id', 'series', 'coin_name', 'series__series_name', 'rate', 'denominal', 'coin_weight', 'coin_thickness', 'coin_diameter', 'photo_obverse', 'photo_reverse', 'manufacture_date', 'item_number', 'link_cbr', 'coin_circulation', 'chemistry', 'description_observe', 'description_reverse', 'painter', 'sculptor', 'coin_herd', 'quality__quality_coinage')
        mints = CoinToMint.objects.filter(coin_id=coin_id).values('mint__mint_name')

        coin_obj = Coins.objects.get(pk = coin_id)
        prices = list(Prices.objects.filter(coin = coin_obj))
        args = {'coin': description, 'mints': mints, 'country': country_id, 'price':prices}

        try:
            args['user_coin'] = UserCoins.objects.filter(user = request.user, coin = coin_id).values('coin', 'coin_series__user_series')
        except:
            args['user_coin'] = []

        try:
            args['wish_list'] = WishListModel.objects.filter(user = request.user, coin = coin_id)
        except:
            args['wish_list'] = {}

        args['chart'] = self.draw_chart(coin_obj)
        rc = RequestContext(request, args)

        return render_to_response(template, rc)

# добавление монеты в коллекцию пользователя

# работа с монетами из списка желаний
class WLView(View):
    template = 'wish_list.html'
    def get(self, request, username):
        rc = self.request_context(request, username)
        return render_to_response(self.template, rc)


    def post(self, request, username):
        wish_id = request.POST.get('wish_id')
        try:
            WishListModel.objects.get(pk=wish_id).delete()
        except:
            print 'Error delete'

        rc = self.request_context(request, username)
        return render_to_response(self.template, rc)

    def request_context(self, request, username):
        args = {}
        wish_list = WishListModel.objects.filter(user_username = username).values('coin__coin_name', 'coin__country', 'coin__id', 'id')

        args['wish_list'] = wish_list
        args['username'] = username
        return RequestContext(request, args)

# добавление монеты в лист желаний
class WishListView(View):
    @method_decorator(login_required)
    def get(self, request):
        coin_id = int(request.GET.get('coin_id'))
        user = request.user

        coin_obj = Coins.objects.get(pk=coin_id)
        try:
            wish_list = WishListModel(user = user, coin = coin_obj, user_username = user.username)
            wish_list.save()
            return  HttpResponse('200', 'plain/text')
        except:
            return  HttpResponse('500', 'plain/text')


