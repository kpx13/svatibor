# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
 

from pages.models import Page

import config
from livesettings import config_value
from django.conf import settings
from catalog.models import Category, Item, Producer
from sessionworking import SessionCartWorking
from shop.forms import OrderForm
from gallery.models import Category as Album
from gallery.models import Photo
from catalog.parse import copy_categories


def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['categories'] = Category.get_top()
    for cat in c['categories']:
        print cat.order_par, cat.name
    c['cart_working'] = SessionCartWorking(request)
    c['cart_count'], c['cart_sum'] = c['cart_working'].get_goods_count_and_sum()
    c.update(csrf(request))
    return c

def page_page(request, page_name):
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
    #[cat.reset_order() for cat in Category.objects.all()]
    #go('/home/kpx/svatibor/3.xml')
    #copy_categories()
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def category(request, slug):
    c = get_common_context(request)
    c['category'] = Category.get_by_slug(slug)
    if not c['category']:
        return page_page(request, slug)
    page = c['category']
    breadcrumbs = []
    while page:
        breadcrumbs.append(page)
        page = page.parent
    breadcrumbs.reverse()
    c['titles'] = breadcrumbs[:-1]
    c['items'] = Item.objects.filter(category=c['category'])
    if len(c['items']) == 0:
        c['items'] = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True))
    return render_to_response('category.html', c, context_instance=RequestContext(request))    

def vendor(request, slug):
    c = get_common_context(request)
    c['category'] = Producer.get_by_slug(slug)
    c['titles'] = []
    c['items'] = Item.objects.filter(producer=c['category'])
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
    c['items'] = c['cart_working'].get_content()
    return render_to_response('cart.html', c, context_instance=RequestContext(request))

def order(request):
    c = get_common_context(request)
    c['items'] = c['cart_working'].get_content()
    if request.method == 'GET':
        c['form'] = OrderForm()
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(request=request)
            c['order'] = order
            return render_to_response('order_ok.html', c, context_instance=RequestContext(request))
        else:
            c['form'] = form
    return render_to_response('order.html', c, context_instance=RequestContext(request))

def add_to_cart(request):
    SessionCartWorking(request).add_to_cart(request.POST['id'], int(request.POST['count']))
    return HttpResponse('')

def recount_cart(request):
    SessionCartWorking(request).recount_cart(request.POST['id'], int(request.POST['count']))
    return HttpResponse('')

def delete_from_cart(request):
    SessionCartWorking(request).del_from_cart(request.POST['id'])
    return HttpResponse('')    

def gallery(request):
    c = get_common_context(request)
    c['gallery'] = Album.objects.all()
    return render_to_response('gallery.html', c, context_instance=RequestContext(request))

def gallery_in(request, slug):
    c = get_common_context(request)
    c['album'] = Photo.objects.filter(category=Album.get_by_slug(slug))
    return render_to_response('gallery_in.html', c, context_instance=RequestContext(request))

def category_old(request, folder_id):
    cat = Category.objects.filter(folder_id=folder_id)
    if len(cat) > 0:
        return HttpResponseRedirect('/category/%s' % cat[0].slug)
    else:
        return HttpResponseRedirect('/')

def item_old(request, product_id):
    item = Item.objects.filter(product_id=product_id)
    if len(item) > 0:
        return HttpResponseRedirect('/item/%s' % item[0].slug)
    else:
        return HttpResponseRedirect('/')
    
def page_old(request, page_name):
    return HttpResponseRedirect('/%s/' % page_name)