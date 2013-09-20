# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
import datetime

from catalog.item import Item
from svatibor.sessionworking import SessionCartWorking


class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name=u'ваше имя')
    organization = models.CharField(max_length=150, blank=True, verbose_name=u'организация')
    phone = models.CharField(max_length=150, verbose_name=u'контактный телефон')
    email = models.CharField(max_length=150, verbose_name=u'контактный e-mail')
    address = models.TextField(blank=True, verbose_name=u'адрес')
    add_info = models.TextField(blank=True, verbose_name=u'дополнительная информация')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата заказа')
    
    
    class Meta:
        verbose_name = u'заказ'
        verbose_name_plural = u'заказы'
        ordering = ['-date']
    
    def __unicode__(self):
        return str(self.date)
    
    def get_count(self):
        return sum([x.count for x in OrderContent.get_content(self)])
    
    def get_sum(self):
        return sum([x.count * x.item.price for x in OrderContent.get_content(self)])
    
        
class OrderContent(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'заказ', related_name='content')
    item = models.ForeignKey(Item, verbose_name=u'товар')
    count = models.IntegerField(default=1, verbose_name=u'количество')
        
    def __unicode__(self):
        return self.item.name
    
    @staticmethod
    def add(order, item, count):
        OrderContent(order=order, item=item, count=count).save()
        
    @staticmethod
    def move_from_cart(request, order):
        cart = SessionCartWorking(request)
        cart_content = cart.pop_content()
        for c in cart_content:
            OrderContent.add(order, c['item'], c['count'])
        
    @staticmethod
    def get_content(order):
        return list(OrderContent.objects.filter(order=order))
    