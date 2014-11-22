from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import RegisterForm


# Create your views here.

class RegistrationForm(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render_to_response('register_success.html')
            #return HttpResponseRedirect('../../coins/')
        else:
            return self.registerPage(request, form)

    def get(self, request):
        form = RegisterForm()
        return self.registerPage(request, form)

    def registerPage(self, request, form):
        args = {}
        args.update(csrf(request))

        args['form'] = form
        return render_to_response('register.html', args)

