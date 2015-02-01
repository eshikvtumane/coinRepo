#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class News(models.Model):
    class Meta:
        db_table = 'News'
        verbose_name = u'Новости'
        verbose_name_plural = u'Новости'

    publisher = models.ForeignKey(User)
    title = models.CharField(u'Заголовок', max_length=255)
    article = models.TextField(u'Статья')
    pub_date = models.DateTimeField(u'Дата публикации', auto_now=True)


class NewsImage(models.Model):
    class Meta:
        db_table = 'NewsImage'
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

    news = models.ForeignKey('News')
    image = models.ImageField(u'Фото', upload_to='news_photo')
