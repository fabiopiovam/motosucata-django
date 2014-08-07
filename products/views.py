# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_managers
from django.conf import settings

from models import Product, type_choices
from forms import ContactForm
from utils import get_query


def index(request):
    product_list    = Product.activated.all()[:9]
    product_banner  = product_list[:1]
    product_list    = product_list[1:8]
    
    template = loader.get_template('products/index.html')
    context = RequestContext(request, {
        'product_banner': product_banner,
        'product_list'  : product_list,
    })
    return HttpResponse(template.render(context))


def search(request, column="", text=""):
    query_string = ''
    product_list = None
    if text.strip():
        if column == 'type':
            type_reverse = dict((v.lower().replace(' ','-'), k) for k, v in type_choices)
            try:
                product_list = Product.activated.filter(type=type_reverse[text])
            except KeyError:
                product_list = None
                
        else:
            query_string = text.replace('-',' ')
            entry_query = get_query(query_string, ['title', 'mark__name', 'model__name', 'description',])
            product_list = Product.activated.filter(entry_query)
    
    template = loader.get_template('products/search_results.html')
    context = RequestContext(request, {
        'query_string': query_string, 
        'product_list': product_list,
    })
    return HttpResponse(template.render(context))


def details(request, slug):
    try:
        product = Product.activated.get(slug=slug)
    except ObjectDoesNotExist:
        product = None
    
    try:
        http_referer = request.environ['HTTP_REFERER']
    except KeyError:
        http_referer = '/'
    
    mail_sent = None
    
    if request.method == 'POST':
        http_referer = request.POST['http_referer']
        
        form = ContactForm(request.POST)
        
        if form.is_valid():
            subject = u'Interesse em ' + product.title
            url     = request.build_absolute_uri()
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            phone   = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            message = u'Mensagem enviada por %s <%s> %s \n\n%s \n\n\nMensagem enviada através da página:\n%s' % (name, email, phone, message, url)
            
            try:
                mail_managers(subject, message, fail_silently = False)
                mail_sent = True
            except Exception as e:
                mail_sent = False
                if settings.DEBUG:
                    raise # reraises the exception
    else:
        form = ContactForm()
    
    template = loader.get_template('products/details.html')
    context = RequestContext(request, {
        'product'   : product,
        'form'      : form,
        'mail_sent' : mail_sent,
        'http_referer' : http_referer,
    })
    return HttpResponse(template.render(context))


def contact(request):
    
    mail_sent = None
    
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
        if form.is_valid():
            url     = request.build_absolute_uri()
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            phone   = form.cleaned_data['phone']
            subject = u'Contato de ' + name
            message = form.cleaned_data['message']
            message = u'Mensagem enviada por %s <%s> %s \n\n%s \n\n\nMensagem enviada através da página:\n%s' % (name, email, phone, message, url)
            
            try:
                mail_managers(subject, message, fail_silently = False)
                mail_sent = True
            except Exception as e:
                mail_sent = False
                if settings.DEBUG:
                    raise # reraises the exception
    else:
        form = ContactForm()
    
    template = loader.get_template('products/contact.html')
    context = RequestContext(request, {
        'form'      : form,
        'mail_sent' : mail_sent,
    })
    return HttpResponse(template.render(context))