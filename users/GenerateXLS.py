import xlwt
import datetime
from django.http import HttpResponse
from models import UserCountries

class GenerateXls():
    def __init__(self, user):
        self.user = user

    def generateUserCollection(self):
        wb = xlwt.Workbook(encoding='utf-8')


        uc = UserCountries.objects.filter(user = self.user).values('id', 'country__country_name')
        for country in uc:
            ws = wb.add_sheet(country['country__country_name'])

        name_file = '%s_%s' % (self.user.username, str(datetime.datetime.today()))
        response = self.createResponse(name_file)
        wb.save(response)
        return response

    def createResponse(self, name_file):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content_Disposition'] = 'attachment; filename=%s.xls' % name_file
        return response

