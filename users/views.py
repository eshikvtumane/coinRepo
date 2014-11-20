from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import RegisterForm


# Create your views here.

class RegistrationForm():
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/index.html')

    def get(self, request):
        args = {}
        args.update(csrf(request))

        args['form'] = RegisterForm()
        return render_to_response('register.html', args)