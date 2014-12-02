#-*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.core import serializers

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from models import Countries, Series, Qualities, Metals, Coins

#from django_ajax.mixin import AJAXMixin # https://github.com/yceruto/django-ajax
#import django_ajax.shortcuts
#
# Create your views here.
def index(request):
    return render(request,'coins/home.html')

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
        args = {'series':series, 'qualities':qualities, 'metals':metals}
        return render_to_response(template_name, args)


class SearchView(View):
    template_name = 'catalog/catalog.html'
    model = Series

    def get(self, request):
        return {'text':'Message from server'}

    def post(self, request):
        if self.request.is_ajax():
            series = request.POST['series']
            name = request.POST.get('name')
            obj = Coins.objects.filter(series_id=series)
            data = serializers.serialize('json', obj, fields=('coin_name', 'photo_obverse', 'rate', 'denominal'))
            return HttpResponse(data, content_type='application/json')
