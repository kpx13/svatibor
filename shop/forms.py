# -*- coding: utf-8 -*-
 
from django.forms import ModelForm
from models import Order, OrderContent
from django.core.mail import send_mail
from django.conf import settings
from django.template import Context, Template


def sendmail(subject, body):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_SEND_TO])
    

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('date', )
        
        
    def save(self, request, *args, **kwargs):
        o = super(OrderForm, self).save(*args, **kwargs)
        OrderContent.move_from_cart(request, o)
        subject=u'Поступил новый заказ.',
        body_templ=u""" 

Имя: {{ o.name }}
Организация: {{ o.organization }}
Телефон: {{ o.phone }}
Емейл: {{ o.email }}
Адрес: {{ o.address }}
Дополнительная информация: {{ o.add_info }}
Дата заказа: {{ o.date }}

--------------------------------------------------------------
Содержимое:
    {% for c in o.content.all %}
        Товар: /item/{{ c.item.id }}, {{ c.count }} шт. по цене {{ c.item.price }} руб.
    {% endfor %}
--------------------------------------------------------------
Всего позиций: {{ o.get_count }} шт.
Общая стоимость:  {{ o.get_sum }} руб. 
"""
        body = Template(body_templ).render(Context({'o': o}))
        sendmail(subject, body)  
        return o  