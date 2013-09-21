# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Category, Photo

class PhotoInline(admin.TabularInline): 
    list_display = ('image', )
    model = Photo
    extra = 10
    
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ PhotoInline, ]
    list_display = ('name', )

admin.site.register(Category, CategoryAdmin)