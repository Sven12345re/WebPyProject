import datetime
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product

# get()
print('----- get() -----')
product = Product.objects.get(id=7)
print('id=7', product, product.user)
