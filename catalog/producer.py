# -*- coding: utf-8 -*-

import pytils
from django.db import models
from ckeditor.fields import RichTextField

class Producer(models.Model):
    name = models.CharField(max_length=512, verbose_name=u'название')
    #logo = models.ImageField(upload_to='uploads/producer', max_length=256, null=True, blank=True, verbose_name=u'логотип')
    #image = models.ImageField(upload_to='uploads/producer', max_length=256, null=True, blank=True, verbose_name=u'изображение')
    description = models.TextField(default=u'', verbose_name=u'описание короткое')
    #text = RichTextField(default=u'У товара нет подробного описания.', verbose_name=u'описание подробное')
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'Заполнять не нужно')
    vendor_id = models.CharField(max_length=20, blank=True, verbose_name=u'vendor_id со старого сайта')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Producer, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Producer.objects.get(slug=page_name)
        except:
            return None
        
    @staticmethod
    def get_or_create(name):
        try:
            pr = Producer.objects.get(name=name)
            return pr
        except:
            pr = Producer(name=name)
            pr.save()
            return pr
    
    
    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'
        ordering=['name']
        
    def __unicode__(self):
        return self.slug
