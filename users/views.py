#-*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import RegisterForm, AuthForm
from django.template import RequestContext


# Create your views here.

class UserRegistration(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render_to_response('users/register_success.html')
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
        return render_to_response('users/register.html', args)

class UserAuth(View):
    def get(self, request):
        form = AuthForm()
        return self.authPage(request, form)

    def post(self, request):
        form = AuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')

        return self.authPage(request, form, 'Вы неверно ввели логин и/или пароль')


    def authPage(self, request, form, error=''):
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['error'] = error

        return render_to_response('users/auth.html', args)

class UserLogout(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect('/')

class UserProfile(View):
    def get(self, request):
        c = RequestContext(request)
        return render_to_response("users/profile.html",c)
