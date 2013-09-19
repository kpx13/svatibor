# -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'название')
    
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'галлерея'
    
    def __unicode__(self):
        return self.title

class Photo(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория', related_name='photos')
    image = models.ImageField(upload_to= 'uploads/gallery', max_length=256, verbose_name=u'картинка')
    
    class Meta:
        verbose_name = u'фотография'
        verbose_name_plural = u'фотографии'
    
    def __unicode__(self):
        return str(self.id)