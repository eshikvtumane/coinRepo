from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext

from news.models import News

# Create your views here.
class HomeView(View):
    def get(self, request):
        template = 'main/home.html'
        args = {}
        news = list(News.objects.filter().order_by('-pub_date')[:10])
        args['news'] = news
        return render_to_response(template, RequestContext(request, args))

