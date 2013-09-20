# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^$', views.home),
    url(r'^cart/$', views.cart),
    url(r'^order/$', views.order),
    url(r'^ajax/add_to_cart/$', views.add_to_cart),
    url(r'^ajax/recount_cart/$', views.recount_cart),
    url(r'^ajax/delete_from_cart/$', views.delete_from_cart),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category),
    url(r'^item/(?P<slug>[\w-]+)/$', views.item),
    url(r'^(?P<page_name>[\w-]+)/$' , views.page),
)
