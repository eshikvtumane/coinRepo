from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext

# Create your views here.
class HomeView(View):
    def get(self, request):
        template = 'main/home.html'
        return render_to_response(template, RequestContext(request))

