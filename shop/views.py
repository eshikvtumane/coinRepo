#-*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import View
from models import SellerPaymentDetal, ShopItem, CoinToShop, ImageCoin, BuyerAddress
from coins.models import Coins

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

import json
from django.core import serializers

from django.core.files import File
from django.conf import settings


# Create your views here.
class SellerSettings(View):
    html = 'settings.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        args = {}

        try:
            pay_detals = SellerPaymentDetal.objects.filter(user=user)
            args['pay'] = pay_detals
        except:
            args['pay'] = []

        return render_to_response(self.html, RequestContext(request, args))

    def post(self, request):

        user = request.user
        number_card = request.POST['number_card']
        ya_money = request.POST['yandex_money']

        datadict = {'number_card' : number_card, 'yandex_money' : ya_money}
        pay_detals, created = SellerPaymentDetal.objects.update_or_create(user = user,defaults=datadict )

        args = {}
        args['pay'] = SellerPaymentDetal.objects.filter(user=user)
        return render_to_response(self.html, RequestContext(request, args))

class CreateLot(View):
    @method_decorator(login_required)
    def get(self, request):
        html = 'create_buy_items.html'
        return render_to_response(html, RequestContext(request, {}))

    def post(self, request):
        user = request.user
        q_lots = request.POST.get('quantity_lots')
        desc = request.POST.get('desc')
        items = json.loads(request.POST.get('items'))

        print '='*40
        photos = json.loads(request.POST['photo'])
        print photos
    # Создание лота продавца
        lot_create = ShopItem(user=user,quantity_lots=q_lots, description=desc)
        lot_create.save()
    # Добавление монет в лот
        coins_sale = [CoinToShop(item=lot_create, coin=Coins.objects.get(pk=i['id']), quantity=i['quantity'], price=i['pay']) for i in items]
        CoinToShop.objects.bulk_create(coins_sale)
    # Добавление фотографий монет продавца
        #file_content = SimpleUploadedFile('%s'%)
        photo = []
        for p in photos:
            path = self.save_file(p)
            photo.append([ImageCoin(item=lot_create, image=path)])
        ImageCoin.objects.bulk_create(photo)
        return HttpResponse('200', 'text/plain')

    def save_file(self, file, path = 'user_image'):
        filename = file._get_name()
        image = '%s/%s' % (settings.MEDIA_ROOT, str(path) + str(filename))
        fd = open(image, 'wb')
        for chunk in file.chunks():
            fd.write(chunk)
        fd.close()
        return image


class SearchCoinsView(View):
    def get(self, request):
        coin_name = request.GET['name'].rstrip()

        coins = Coins.objects.filter(coin_name__contains=coin_name).only('id', 'rate', 'denominal', 'coin_name', 'photo_obverse')
        data = serializers.serialize('json', coins)
        json_coins = json.dumps(data)
        return HttpResponse(json_coins, content_type='application/json')


# работа с адресом для доставки
class DeliveryAddressView(View):
    html = 'user_address.html'

    @method_decorator(login_required)
    def get(self, request):
        args = {}
        user = request.user
        dict_address = self.getAddress(user)
        args = dict_address
        return render_to_response(self.html, RequestContext(request, args))

    def post(self, request):
        region = request.POST.get('region')
        city = request.POST.get('city')
        street = request.POST.get('street')
        building = request.POST.get('building')
        housing = request.POST.get('housing')
        structure = request.POST.get('structure')
        flat = request.POST.get('flat')
        zip = request.POST.get('zip')
        user = request.user

        args = {}

        try:
            ba = BuyerAddress(buyer = user, city=city, zip_code=zip, region=region, street = street, house = building, housing = housing,  structure = structure, flat = flat)
            ba.save()
        except:
            print 'Error'

        user = request.user
        args = self.getAddress(user)

        return render_to_response(self.html, RequestContext(request, args))

    def getAddress(self, user):
        args = {}
        args['address'] = BuyerAddress.objects.filter(buyer = user)
        return args
