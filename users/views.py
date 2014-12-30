#-*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import auth
from django.core.context_processors import csrf
from users.forms import RegisterForm, AuthForm, UserProfileForm, CustomUserForm
from django.template import RequestContext

from django.core import serializers
import json

from django.contrib.auth.models import User
from coins.models import Countries, Series, Coins, CoinToMint, Mints
from users.models import Profile, UserCountries, UserSeries as US, UserCoins, UserCoinInfo, Defects, CoinsCondition

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


class UserCountryView(View):
    #Выборка стран, которые выбрал пользователь
    @method_decorator(login_required)
    def get(self, request):
        html = 'collections/select_country.html'
        args = {}
        try:
            countries_user = UserCountries.objects.filter(user=request.user).values('country', 'country__country_name', 'country__country_flag')
            countries = Countries.objects.all()
            args['countries_user'] = countries_user
            c_id = [ obj['country'] for obj in countries_user ]
            args['countries'] = countries.exclude(id__in = c_id) # ИСКЛЮЧЕНИЕ, ДОБАВЛЕННЫХ ПОЛЬЗОВАТЕЛЕМ, СТРАН
            return render_to_response(html, RequestContext(request, args))
        except:
            return render_to_response(html, RequestContext(request, {'countries': []}))

# добавление страны к определённому пользователю
    def post(self, request):
        country_id = request.POST['country_id']
        country = Countries.objects.get(pk=country_id)

        try:
            UserCountries.objects.get(user=request.user, country=country)
            return HttpResponse('200', content_type='plain/text')
        except UserCountries.DoesNotExist:
            user_country = UserCountries(user=request.user, country=country)
            user_country.save()


            c = Countries.objects.filter(id=country_id)
            json = serializers.serialize('json', c)
            return HttpResponse(json,content_type='application/json')

# добавление пользователем серий
class UserSeriesView(View):
    @method_decorator(login_required)
    def get(self, request, country_id):
        html = 'collections/select_series.html'
        series = Series.objects.filter(country=country_id)
        try:
            # ищем страны
            country = UserCountries.objects.get(country=country_id)

            # ищем страны, которые добавил пользователь и отправляем всё клиенту
            try:
                series_user = US.objects.filter(user=request.user, user_country=country).values('user_series__series_name', 'user_series')
                s = [ obj['user_series'] for obj in series_user ]
                series = series.exclude(id__in = s)
                return render_to_response(html, RequestContext(request, {'series_user':series_user, 'series':series, 'country': {'id':country_id,'name':country}}))
            except:
                print 'Error'
                return render_to_response(html, RequestContext(request, {'series':series, 'country': {'id':country_id,'name':country}}))
        except Countries.DoesNotExist:
            raise Http404


    def post(self, request):
        series_id = request.POST['series_id']
        country_id = request.POST['country_id']
        s = Series.objects.get(pk=series_id)
        c = UserCountries.objects.get(country=country_id)

        try:# если пользователь уже добавил серию
            US.objects.get(user_series=s,user = request.user, user_country=c)
            return HttpResponse('200', content_type='plain/text')
        except US.DoesNotExist:# если пользователь ещё не добавил серию
            usr_series = US(user = request.user, user_series=s,user_country=c)
            usr_series.save()
            return HttpResponse('400', content_type='plain/text')

# работаем с монетами пользователя
class UserCoinsView(View):
    @method_decorator(login_required)
    def get(self, request, country_id, series_id):
        template = 'collections/select_coins.html'
        args = {}
        args['series'] = series_id

        try:
            args['series_name'] = Series.objects.get(id = series_id)
        except Series.DoesNotExist:
            raise Http404

        try:
            coins = Coins.objects.filter(series=series_id).values('coin_name', 'id').order_by('coin_name')
            series = US.objects.get(user_series = series_id)
            args['coins'] = coins
            try: # делаем выборку монет, которые добавил пользователь
                user_coins = UserCoins.objects.filter(user=request.user, coin_series=series).values('coin__photo_reverse', 'coin__coin_name', 'coin__id').order_by('coin__coin_name')
                us = [ obj['coin__id'] for obj in user_coins ]
                args['coins'] = coins.exclude(id__in = us) # исключаем те монеты, которые уже есть у пользователя
                args['usr_coins'] = user_coins
                return render_to_response(template, RequestContext(request, args))
            except UserCoins.DoesNotExist: # Если пользователь ничего не добавил, то ничего и не выбираем из БД
                return render_to_response(template, RequestContext(request, args))
        except Coins.DoesNotExist: # если монет с таким id нет, то вызываем 404
            raise Http404

# добавляем выбранные монеты
    def post(self, request):
        coins = json.loads(request.POST['coins'])

        series = request.POST['id']

        # Делаем выборку по монетам и сериям
        coins_obj = Coins.objects.filter(id__in=coins)
        series_obj = US.objects.get(user_series=series)

        # генерируем массив пользовательских монет
        usr_objs = [ UserCoins(user=request.user, coin_series=series_obj, coin=coin) for coin in coins_obj ]
        # разом отсылаем массив в БД
        UserCoins.objects.bulk_create(usr_objs)

        c = coins_obj
        print c
        json_obj = serializers.serialize('json', c)
        return HttpResponse(json_obj, content_type='plain/text')

# добавляем разновидности монет
class UserCoinInfoView(View):
    def get(self, request, country_id, series_id, coin_id):
        template = 'collections/add_coins.html'
        try:
            args = self.get_UserCoinInfo(request.user, coin_id, country_id, series_id)

            return render_to_response(template, RequestContext(request, args))
        except UserCoins.DoesNotExist:
            return render_to_response(template, RequestContext(request))

    def post(self, request, country_id, series_id, coin_id):
        template = 'collections/add_coins.html'
        request_user = request.user

        user_coin = UserCoins.objects.get(user = request_user, coin = coin_id)
        quantity = request.POST['quantity']
        mint = Mints.objects.get(pk=request.POST['mint'])
        condition = CoinsCondition.objects.get(pk=request.POST['condition'])
        defect = Defects.objects.get(pk=request.POST['defect'])
        note = request.POST['note']
        args = {}

        try:
            uc = UserCoinInfo(user = request_user, coin_user = user_coin, quantity = quantity, mint = mint, condition = condition, defect_type = defect, note = note)
            uc.save()
            uci = self.get_UserCoinInfo(request.user, coin_id, country_id, series_id)
            args = uci
            return render_to_response(template, RequestContext(request, args))
        except:
            uci = self.get_UserCoinInfo(request_user, coin_id, country_id, series_id)
            args['uci'] = uci
            return render_to_response(template, RequestContext(request, args))

    def get_UserCoinInfo(self, user, coin_id, country_id, series_id):
        uc = UserCoins.objects.get(user = user, coin = coin_id)
        uci = UserCoinInfo.objects.filter(coin_user = uc).values('id', 'condition__condition_name', 'condition__condition_color', 'quantity', 'mint__mint_abbreviation', 'mint__mint_name', 'defect_type__defect_name', 'note')

        mints = CoinToMint.objects.filter(coin=coin_id).values('mint__id', 'mint__mint_abbreviation')
        defects = Defects.objects.all()
        condition = CoinsCondition.objects.all()
        coin = Coins.objects.get(pk=coin_id)

        series = Series.objects.filter(id=series_id).values('id', 'series_name', 'country__id', 'country__country_name')

        return { 'uci': uci, 'mints': mints, 'defects': defects, 'conditions': condition, 'coin': coin, 'country': country_id, 'series': series }


# Удаление страны, серии, монеты
class DeleteView(View):
    def delete(self, request, model, userModel, obj_del, id):
        try:
            c = model.objects.filter(id=id)
            obj_del.delete()
            json_obj = serializers.serialize('json', c)

            return HttpResponse(json_obj, 'application/json')
        except:
            return HttpResponse('500', 'plain/text')


class SeriesDeleteView(DeleteView):
    def post(self, request):
        series_id, us_mod = request.POST['s_id'], US

        model, userModel, obj_del = Series, us_mod, us_mod.objects.filter(user = request.user, user_series = series_id)
        return self.delete(request, model, userModel, obj_del, series_id)


class CountryDeleteView(DeleteView):
    def post(self, request):
        country_id, us_mod = request.POST['c_id'], UserCountries

        model, userModel, obj_del = Countries, us_mod, us_mod.objects.filter(user = request.user, country = country_id)
        return self.delete(request, model, userModel, obj_del, country_id)


class CoinDeleteView(DeleteView):
    def post(self, request):
        coin_id, us_mod = request.POST['c_id'], UserCoins

        model, userModel, obj_del = Coins, us_mod, us_mod.objects.filter(user = request.user, coin = coin_id)
        return self.delete(request, model, userModel, obj_del, coin_id)


# Обновление значения количества монет и удаление описания монеты
class CoinInfoChangeView(View):
    def http_resp(self, code):
        return HttpResponse(code, 'plain/text')

    def get(self, request):
        q_id = request.GET['quantity']
        coin_id = request.GET['coin']

        try:
            UserCoinInfo.objects.filter(user=request.user, id = coin_id).update(quantity = q_id)
            return self.http_resp('200')
        except:
            return self.http_resp('500')

    def post(self, request):
        coin_id = request.POST['c_id']
        try:
            UserCoinInfo.objects.filter(user = request.user, id = coin_id).delete()
            return HttpResponse('200', 'plain/text')
        except:
            return HttpResponse('500', 'plain/text')