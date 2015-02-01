from django.contrib import admin
from models import News, NewsImage

# Register your models here.
class NewsImageForm(admin.StackedInline):
    model = NewsImage

class NewsAdmin(admin.ModelAdmin):
    inlines = [
        NewsImageForm,
    ]
    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce/textbox.js'
        ]


admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage, )