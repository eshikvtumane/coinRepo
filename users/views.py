#-*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from users.forms import RegisterForm, AuthForm, UserProfileForm, CustomUserForm
from django.template import RequestContext
from django.core import serializers

from models import Profile
from django.contrib.auth.models import User
from coins.models import Countries
from users.models import UserCountries

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

class UserRegistration(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render_to_response('register_success.html', RequestContext(request))
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
        return render_to_response('register.html', RequestContext(request, args))

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

        return render_to_response('auth.html', RequestContext(request, args))

#@login_required
class UserLogout(View):
    @method_decorator(login_required)
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect('/')

# Профайл пользователя
class UserInfo(View):
    @method_decorator(login_required)
    def get(self, request):
        args = {}
        try:
            current_user = request.user.profile
            data = {
                'first_name':current_user.first_name,
                'last_name': current_user.last_name,
                'middle_name': current_user.middle_name,
                'avatar': current_user.avatar
            }
            args['form'] = UserProfileForm(data)
            args['url_image'] = current_user.avatar
        except:
            args['form'] = UserProfileForm()

        args['user_form'] = CustomUserForm()
        args['email'] = request.user.email
        return render_to_response('user_info.html', RequestContext(request, args))

# save information about user
    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm()
        args = {}
        data = {'email':request.user.email}
        email = request.POST['email']
        # проверка: ввёл ли пользователь новый пароль
        if not email:
            # если нет, то оставляем текущий
            email = request.user.email

        # проверка: есть ли в базе профайл пользователя
        try:
            # если есть, то привяжем найденный объект к форме (для обновления данных в базе, иначе orm попробует добавить новую запись)
            user_profile = Profile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        except:
            form = UserProfileForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user

            # обновляем email
            User.objects.filter(pk=request.user.id).update(email=email)
            # добавляем/обновляем пользовательские данные
            user.save()
            return render_to_response('user_info.html', RequestContext(request, {'form':form, 'url_image':user.avatar, 'success':True, 'user_form':CustomUserForm(), 'email': email}))
        else:
            return render_to_response('user_info.html', RequestContext(request, {'form':form, 'url_image':request.user.avatar, 'error':True,'user_form':CustomUserForm(), 'email': email}))


class UserCountry(View):
    #Выборка стран, которые выбрал пользователь
    @method_decorator(login_required)
    def get(self, request):
        html = 'collections/select_country.html'
        args = {}
        try:
            countries_user = UserCountries.objects.filter(user=request.user).values('country', 'country__country_name', 'country__country_flag')
            countries = Countries.objects.all()
            args['countries_user'] = countries_user
            args['countries'] = countries
            return render_to_response(html, RequestContext(request, args))
        except:
            return render_to_response(html, RequestContext(request, {'countries': []}))

# добавление страны к определённому пользователю
    def post(self, request):
        country_id = request.POST['country_id']
        c = Countries.objects.filter(id=country_id)
        country = Countries.objects.get(pk=country_id)

        try:
            UserCountries.objects.get(user=request.user, country=country)
            return HttpResponse('200', content_type='plain/text')
        except UserCountries.DoesNotExist:
            user_country = UserCountries(user=request.user, country=country)
            user_country.save()
            json = serializers.serialize('json', c)
            return HttpResponse(json,content_type='application/json')

