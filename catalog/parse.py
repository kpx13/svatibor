 # -*- coding: utf-8 -*-

import sys
import re
from django.conf import settings
from category import Category
from producer import Producer
from item import Item
from xml.dom import minidom
 
"""
class Item(models.Model): 
    category = models.ForeignKey(Category, verbose_name=u'категория')
    producer = models.ForeignKey(Producer, blank=True, verbose_name=u'производитель')
    name = models.CharField(max_length=512, verbose_name=u'название')
    art = models.CharField(max_length=16, blank=True, verbose_name=u'артикул')
    price = models.FloatField(verbose_name=u'цена')
    image = models.ImageField(upload_to='uploads/items', max_length=256, blank=True, verbose_name=u'изображение')
    description = models.TextField(default=u'', verbose_name=u'описание короткое')
    text = RichTextField(default=u'У товара нет подробного описания.', verbose_name=u'описание подробное')
    stock = models.IntegerField(default=0, verbose_name=u'в наличии')
    is_novelty = models.BooleanField(default=False, blank=True, verbose_name=u'это новинка')
    slug = models.SlugField(max_length=240, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    product_id = models.CharField(max_length=20, blank=True, verbose_name=u'product_id со старого сайта')
"""        

def go_categories(xmldoc):
    categorieslist = xmldoc.getElementsByTagName('category')
    for s in categorieslist:
        category_id = s.attributes['id'].value
        name = s.childNodes[0].nodeValue
        try:
            parent_id = s.attributes['parentId'].value 
        except:
            parent_id = None
        print name
        print Category.get_by_folder_id(parent_id)
        print category_id
        c = Category(name=name.replace('&quot;', '"'),
                 parent=Category.get_by_folder_id(parent_id),
                 folder_id=category_id)
        print c
        c.save()
                 
def go_items(xmldoc):
    itemlist = xmldoc.getElementsByTagName('offer') 
    for s in itemlist :

        product_id = s.attributes['id'].value
        price = s.getElementsByTagName('price')[0].childNodes[0].nodeValue
        name = s.getElementsByTagName('name')[0].childNodes[0].nodeValue
        vendor = s.getElementsByTagName('vendor')[0].childNodes[0].nodeValue
        if s.getElementsByTagName('description')[0].childNodes:
            description = s.getElementsByTagName('description')[0].childNodes[0].nodeValue
        else:
            description = ''
            
        category_id = s.getElementsByTagName('categoryId')[-1].childNodes[0].nodeValue
        producer = Producer.get_or_create(vendor)
        category = Category.get_by_folder_id(category_id)
        if category:
            Item(category=category,
                 producer=producer,
                 name=name,
                 price=float(price),
                 description=description,
                 product_id=product_id,
                 ).save()
def go_desc():
    BASE_URL = 'http://www.svatibor.ru/internet_magazin/product/'
    import urllib2
    from bs4 import BeautifulSoup
    for i in Item.objects.all():
        print BASE_URL + str(i.product_id)
        c = urllib2.urlopen(BASE_URL + str(i.product_id))
        soup = BeautifulSoup(c.read())
        i.text = str(soup.findAll('div', attrs={'class' : 'full'})[0]).replace('\n', '<br />')
        i.stock=100
        i.art = soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('ul', attrs={'id' : 'p_list'})[0].findAll('span')[0].string
        i.is_novelty = len(soup.findAll('li', attrs={'class' : 'new'})) > 0
        image = 'http://www.svatibor.ru' + soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('a')[0]['href']
        if image.endswith('.jpg'):
            f = open('media/uploads/items/%s.jpg' % i.id,'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            i.image = 'uploads/items/%s.jpg' % i.id
        else:
            print image
        i.save()
        
        

def go(filename):
    xmldoc = minidom.parse(filename)
    #go_categories(xmldoc)
    go_items(xmldoc)
    go_desc()
    
FILES = ['d/64379/t/v0/images/col.gif',
         'd/64379/t/v0/images/buy.gif',

        ]
    
def go_static():
    import urllib2
    import os
    STATIC_PATH = 'site_static/'
    SITE_PATH = 'http://www.svatibor.ru/'
    for page_url in FILES:
        try:
            os.makedirs(STATIC_PATH + '/'.join(page_url.split('/')[:-1]))
        except:
            pass
        f = open(STATIC_PATH + page_url, 'wb')
        f.write(urllib2.urlopen(SITE_PATH + page_url).read())
        f.close()
        print page_url
    