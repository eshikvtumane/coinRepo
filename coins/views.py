from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext,Template
from django.http import HttpResponse
from django.core import serializers
from models import Countries
from models import Mints
import json

#
# Create your views here.
def index(request):
    return render_to_response(request,'coins/home.html')

class SearchView(View):
    def get(self,request,*args,**kwargs):
        countries = Countries.objects.all()

        return render_to_response('coins/coin_search.html',{'countries':countries})

def ajax(request):
     country = request.GET["country"]
     mints = list(Mints.objects.filter(country_id=country))
     print mints
     c = RequestContext(request,{'result':serializers.serialize("json",mints)})
     t = Template("{{result|safe}}")
     response = HttpResponse(t.render(c),content_type='application/json')
     return response




