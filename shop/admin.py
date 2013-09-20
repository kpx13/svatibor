# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Order, OrderContent

class ContentInline(admin.TabularInline): 
    list_display = ('item', 'count')
    model = OrderContent
    extra = 5
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [ ContentInline, ]
    list_display = ('date', )

admin.site.register(Order, OrderAdmin)