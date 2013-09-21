# -*- coding: utf-8 -*-

import pytils
from django.db import models
from ckeditor.fields import RichTextField

from producer import Producer
from category import Category

class Item(models.Model): 
    category = models.ForeignKey(Category, verbose_name=u'категория')
    producer = models.ForeignKey(Producer, blank=True, verbose_name=u'производитель')
    name = models.CharField(max_length=512, verbose_name=u'название')
    art = models.CharField(max_length=50, blank=True, verbose_name=u'артикул')
    price = models.FloatField(verbose_name=u'цена')
    image = models.ImageField(upload_to='uploads/items', max_length=256, blank=True, verbose_name=u'изображение')
    description = models.TextField(default=u'', verbose_name=u'описание короткое')
    text = RichTextField(default=u'У товара нет подробного описания.', verbose_name=u'описание подробное')
    stock = models.IntegerField(default=0, verbose_name=u'в наличии')
    is_novelty = models.BooleanField(default=False, blank=True, verbose_name=u'это новинка')
    slug = models.SlugField(max_length=240, verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    product_id = models.CharField(max_length=20, blank=True, verbose_name=u'product_id со старого сайта')
    
    
    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        if not self.slug:
            self.slug= str(self.category.slug)+ '_' + pytils.translit.slugify(self.name) + '_' + str(self.id)
            self.slug = self.slug[:100]
            self.save()
        
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Item.objects.get(slug=page_name)
        except:
            return None
        
    @staticmethod
    def get(id):
        try:
            return Item.objects.get(id=id)
        except:
            return None

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering=['id']
        
    def __unicode__(self):
        return self.name