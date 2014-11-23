from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import HttpResponse
from models import Countries

#
# Create your views here.
def index(request):
    return render(request,'coins/home.html')

class SearchView(View):
    def get(self,request,*args,**kwargs):
        countries = Countries.objects.all()

        return render_to_response('coins/coin_search.html',{'countries':countries})