# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings

from models import Product
from forms import ContactForm


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


def details(request, slug):
    try:
        product = Product.activated.get(slug=slug)
    except ObjectDoesNotExist:
        product = None
    
    mail_sent = None
    
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.get_host() + u' - Interesse em ' + product.title
            url     = request.build_absolute_uri()
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            phone   = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            message = u'Mensagem enviada por %s <%s> - %s \n\n%s \n\n\nMensagem enviada através da página:\n%s' % (name, email, phone, message, url)
            
            mail_from   = settings.DEFAULT_FROM_EMAIL
            recipients  = [settings.EMAIL_HOST_USER]
            
            mail_sent = send_mail(subject, message, mail_from, recipients, fail_silently=True)
    else:
        form = ContactForm()
    
    template = loader.get_template('products/details.html')
    context = RequestContext(request, {
        'product'   : product,
        'form'      : form,
        'mail_sent' : mail_sent,
    })
    return HttpResponse(template.render(context))