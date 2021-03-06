# -*- coding: utf-8 -*-
import pytils
from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    name = models.CharField(max_length=512, verbose_name=u'название')
    content = RichTextField(blank=True, verbose_name=u'контент')
    slug = models.CharField(verbose_name=u'слаг', max_length=200, unique=True, blank=True, help_text=u'Заполнять не нужно')
    folder_id = models.CharField(max_length=20, blank=True, verbose_name=u'folder_id со старого сайта')
    order_par = models.IntegerField(max_length=20, blank=True, default=666, verbose_name=u'порядок сортировки')
    
    def reset_slug(self):
        if self.parent:
            self.parent.reset_slug()
            self.slug = self.parent.slug + '/' + pytils.translit.slugify(self.name)
        else:
            self.slug = pytils.translit.slugify(self.name)
        self.save()
    
    def reset_order(self):
        self.order_par = self.id
        self.save()
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.slug:
            if self.parent:
                self.slug = self.parent.slug + '/' + pytils.translit.slugify(self.name)
            else:
                self.slug = pytils.translit.slugify(self.name)
            self.save()
        if not self.order_par:
            self.order_par = self.id
            self.save()
        
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Category.objects.get(slug=page_name)
        except:
            return None
    
    @staticmethod
    def get_by_folder_id(folder_id):
        if folder_id:
            try:
                return Category.objects.get(folder_id=folder_id)
            except:
                return None
        else:
            return None
        
    @staticmethod
    def get_top():
        return Category.objects.filter(parent=None).order_by('order_par')
        
    class MPTTMeta:
        order_insertion_by = ['name']
        
    def __unicode__(self):
        return '%s%s' % (' -- ' * self.level, self.name)
    
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        
    