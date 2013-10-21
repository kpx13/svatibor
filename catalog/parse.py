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
        elif image.endswith('.png'):
            f = open('media/uploads/items/%s.png' % i.id,'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            i.image = 'uploads/items/%s.png' % i.id
            print image
        i.save()
        
        

def go(filename):
    xmldoc = minidom.parse(filename)
    #go_categories(xmldoc)
    go_items(xmldoc)
    go_desc()
    
FILES = ['d/64379/d/rules-logo_1.jpg',
         'd/64379/d/rules-pic.jpg',
         'd/64379/d/vika-logo_1.jpg',
         'd/64379/d/vika-pic.jpg',
         'd/64379/d/onix-logo_1.jpg',
         'd/64379/d/onix-pic.jpg',
         'd/64379/d/top-logo_1.jpg',
         'd/64379/d/top-pic.jpg',
         'd/64379/d/arch-logo.jpg',
         'd/64379/d/arch-pic.jpg',
         'd/64379/d/sillur-logo.jpg',
         'd/64379/d/sillur-pic.jpg',
         'd/64379/d/hart-logo.jpg',
         'd/64379/d/harct-pic.jpg',
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
    
def go_images():
    BASE_URL = 'http://www.svatibor.ru/internet_magazin/product/'
    import urllib2
    import os
    from bs4 import BeautifulSoup
    for i in Item.objects.filter(image=''):
        print BASE_URL + str(i.product_id)
        c = urllib2.urlopen(BASE_URL + str(i.product_id))
        soup = BeautifulSoup(c.read())
        image = 'http://www.svatibor.ru' + soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('a')[0]['href']
        if image.endswith('.png'):
            f = open('media/uploads/items/%s.png' % i.id,'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            i.image = 'uploads/items/%s.png' % i.id
            i.save()
        else:
            print image
        

GALLERY = [(1, 'http://www.svatibor.ru/nashi-vystavki/album/411603'),
           (2, 'http://www.svatibor.ru/nashi-vystavki/album/411803'),
           (3, 'http://www.svatibor.ru/nashi-vystavki/album/412003'),
           (4, 'http://www.svatibor.ru/nashi-vystavki/album/500803'),
           (5, 'http://www.svatibor.ru/nashi-vystavki/album/501003')
           ]

def go_gallery():
    import urllib2
    from bs4 import BeautifulSoup
    from gallery.models import Category as Album
    from gallery.models import Photo
    for album, url in GALLERY:
        cat = Album.objects.get(id=album)
        c = urllib2.urlopen(url)
        soup = BeautifulSoup(c.read())
        table = soup.findAll('table', attrs={'class' : 'gallery2_album_photos'})[0]
        for td in table.findAll('td'):
            img = td.findAll('img')[0]
            image = 'http://www.svatibor.ru' + td.findAll('a')[0]['href']
            filepath = 'uploads/gallery/%s' % image.split('/')[-1]
            f = open('media/%s' % filepath, 'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            Photo(category=cat,
                  name=img['alt'],
                  image=filepath).save()
            print img['alt'] 


import urllib2
from bs4 import BeautifulSoup

def copy_categories():
    LIST_URL = 'http://www.svatibor.ru/internet_magazin/folder/24738403'
    c = urllib2.urlopen(LIST_URL)
    soup = BeautifulSoup(c.read())
    CATEGORIES = []
    for div in soup.findAll('div', attrs={'class' : 'tovar'}):
        prod = div.findAll('h2')[0].findAll('a')[0]['href']
        CATEGORIES.append(prod)

    BASE_URL = 'http://www.svatibor.ru'
    
    for url in CATEGORIES:
        print BASE_URL + url
        cat = Category.objects.get(id=26)
        prod = Producer.objects.get(id=9)
        c = urllib2.urlopen(BASE_URL + url)
        soup = BeautifulSoup(c.read())
        text = str(soup.findAll('div', attrs={'class' : 'full'})[0]).replace('\n', '<br />')
        stock=100
        art = soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('ul', attrs={'id' : 'p_list'})[0].findAll('span')[0].string
        price = soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('li', attrs={'class': 'price'})[0].findAll('span')[0].findAll('b')[0].string
        name = soup.findAll('div', attrs={'id' : 'tovar_detail'})[0].findAll('h1')[0].string
        is_novelty = len(soup.findAll('li', attrs={'class' : 'new'})) > 0
        image = 'http://www.svatibor.ru' + soup.findAll('div', attrs={'id' : 'tovar_card'})[0].findAll('a')[0]['href']
        i = Item(category=cat,
            name=name,
            price=price,
            producer = prod,
            description=u'цена за полотно',
            product_id=url,
            text=text,
            stock=stock,
            art=art,
            is_novelty=is_novelty
            )
        i.save()
        if image.endswith('.jpg'):
            f = open('media/uploads/items/%s.jpg' % i.id,'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            i.image = 'uploads/items/%s.jpg' % i.id
        elif image.endswith('.png'):
            f = open('media/uploads/items/%s.png' % i.id,'wb')
            f.write(urllib2.urlopen(image).read())
            f.close()
            i.image = 'uploads/items/%s.png' % i.id
        else:
            print 'ERROR: ', image
        i.save()
    
 