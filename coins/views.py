#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View, TemplateView
from django.template import RequestContext,Template

from django.core.context_processors import csrf
from django.core import serializers
import json

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from models import Countries, Series, Qualities, Metals, Coins, Mints, CoinToMint

from django.db.models import Q # http://proft.me/2011/01/22/polnotekstovyj-poisk-v-django/
import operator
#from django_ajax.mixin import AJAXMixin # https://github.com/yceruto/django-ajax
#import django_ajax.shortcuts

#http://django-haystack.readthedocs.org/en/latest/tutorial.html
from haystack.query import SearchQuerySet
import json

#
# Create your views here.
def index(request):
    return render_to_response(request,'coins/home.html')


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
        args['countries'] = countries
        return render_to_response('catalog/catalog.html', args)

class CoinsView(View):

    def get(self, request, country_id):
        template_name = 'catalog/coins.html'
        series = Series.objects.filter(country_id=country_id)
        qualities = Qualities.objects.all()
        metals = Metals.objects.all()
        coins = Coins.objects.order_by('?')[0:15] # select random coins objects
        args = {'series':series, 'qualities':qualities, 'metals':metals, 'coins':coins}
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

            criterions = []
            if not number:
                if series != '':
                    criterions.append(Q(series_id=series),)
                if name != '':
                    criterions.append(Q(coin_name=name),)
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
        template = 'catalog/coin_descr.html'
        coin_id = int(coin_id)
        description = Coins.objects.filter(id=coin_id).values('coin_name', 'series__series_name', 'rate', 'denominal', 'coin_weight', 'coin_thickness', 'coin_diameter', 'photo_obverse', 'photo_reverse', 'manufacture_date', 'item_number', 'link_cbr', 'coin_circulation', 'chemistry', 'description_observe', 'description_reverse', 'painter', 'sculptor', 'coin_herd', 'quality__quality_coinage')
        mints = CoinToMint.objects.filter(coin_id=coin_id).values('mint__mint_name')
        return render_to_response(template, {'coin': description, 'mints': mints})