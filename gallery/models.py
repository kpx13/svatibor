# -*- coding: utf-8 -*-
from django.db import models
import pytils

class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    description = models.TextField(blank=True, verbose_name=u'описание')
    slug = models.SlugField(verbose_name=u'слаг', max_length=200, unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Category.objects.get(slug=page_name)
        except:
            return None
    
    class Meta:
        verbose_name = u'альбом'
        verbose_name_plural = u'галерея'
    
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория', related_name='photos')
    image = models.ImageField(upload_to= 'uploads/gallery', max_length=256, verbose_name=u'картинка')
    name = models.CharField(max_length=200, verbose_name=u'название')
    
    class Meta:
        verbose_name = u'фотография'
        verbose_name_plural = u'фотографии'
    
    def __unicode__(self):
        return str(self.id)