# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
 

from pages.models import Page

import config
from livesettings import config_value
from django.conf import settings
from catalog.models import Category, Item


def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['categories'] = Category.objects.filter(parent=None).extra(order_by = ['id'])
    c.update(csrf(request))
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get_by_slug(page_name)
    if p:
        c.update({'p': p})
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        raise Http404()

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    from catalog.parse import go_static
    go_static()
    #go('/home/kpx/svatibor/3.xml')    
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def category(request, slug):
    c = get_common_context(request)
    c['category'] = Category.get_by_slug(slug)
    page = c['category']
    breadcrumbs = []
    while page:
        breadcrumbs.append(page)
        page = page.parent
    breadcrumbs.reverse()
    c['titles'] = breadcrumbs[:-1]
    c['items'] = Item.objects.filter(category=c['category'])
    return render_to_response('category.html', c, context_instance=RequestContext(request))

def item(request, slug):
    c = get_common_context(request)
    item = Item.get_by_slug(slug)
    c['category'] = item.category
    page = c['category']
    breadcrumbs = []
    while page:
        breadcrumbs.append(page)
        page = page.parent
    breadcrumbs.reverse()
    c['titles'] = breadcrumbs
    c['item'] = item
    return render_to_response('item.html', c, context_instance=RequestContext(request))

def cart(request):
    c = get_common_context(request)
    return render_to_response('cart.html', c, context_instance=RequestContext(request))

def order(request):
    c = get_common_context(request)
    return render_to_response('order.html', c, context_instance=RequestContext(request))    