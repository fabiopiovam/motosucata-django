from django.http import HttpResponse
from django.template import RequestContext, loader

from models import Product

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