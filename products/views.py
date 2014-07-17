from django.http import HttpResponse
from django.template import RequestContext, loader

from models import Product

def index(request):
    product_list = Product.objects.order_by('-created_at')[:10]
    template = loader.get_template('products/index.html')
    context = RequestContext(request, {
        'product_list': product_list,
    })
    return HttpResponse(template.render(context))