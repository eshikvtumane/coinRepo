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

from django.conf import settings
import os
import datetime


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

    # Создание лота продавца
        lot_create = ShopItem(user=user,quantity_lots=q_lots, description=desc, total_sum=0)
        lot_create.save()
    # Добавление монет в лот
        total_sum = 0
        coins_sale = []
        for i in items:
            coins_sale.append(CoinToShop(item=lot_create, coin=Coins.objects.get(pk=i['id']), quantity=i['quantity'], price=i['pay']))
            total_sum += int(i['pay'])

        lot_create.total_sum = total_sum
        lot_create.save()

        CoinToShop.objects.bulk_create(coins_sale)
    # Добавление фотографий монет продавца
        fuv = FileUploadView()
        img_obj = fuv.add_image(request, 'user_image', 'coinson', lot_create)

        ImageCoin.objects.bulk_create(img_obj)
        return HttpResponse('200', 'text/plain')


# загрузка файлов
class FileUploadView():
    def add_image(self, request, UPLOAD_TO, FILENAME, LOT_ID):
        print request.FILES
        if request.FILES and request.FILES.get('file'):
            return self.__save_file(UPLOAD_TO,
                             request.FILES.getlist('file'),
                             FILENAME,
                             LOT_ID)


        return []

    def __save_file(self, dest_path, files, filename, lot_item):
        imagecoin_obj = []
        for f in files:
            original_name, file_extension = os.path.splitext(f.name)
            filename = filename + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + file_extension
            url = dest_path + '/' + filename
            path = settings.MEDIA_ROOT + url
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            imagecoin_obj.append(ImageCoin(item = lot_item, image=path))
        return imagecoin_obj


class SearchCoinsView(View):
    def get(self, request):
        coin_name = request.GET['name'].rstrip()

        coins = Coins.objects.filter(coin_name__contains=coin_name).only('id', 'rate', 'denominal', 'coin_name', 'photo_obverse')
        data = serializers.serialize('json', coins)
        json_coins = json.dumps(data)
        return HttpResponse(json_coins, content_type='application/json')


class LotsView(View):
    html = 'view_lots.html'
    def get(self, request):
        args = {}

        args['lots'] = ShopItem.objects.filter().values('id', 'user__username', 'quantity_lots', 'description', 'total_sum')
        args['items'] = CoinToShop.objects.all().values('item', 'quantity', 'price', 'coin__photo_reverse', 'coin__coin_name', 'coin__country__id', 'coin__id', 'coin__denominal', 'coin__rate')
        #args['lots'] = CoinToShop.objects.all()
        return render_to_response(self.html, RequestContext(request, args))

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


