# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Producer, Category, Item


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'slug')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('art', 'name', 'category', 'price', 'stock', 'is_novelty')

admin.site.register(Producer, ProducerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)