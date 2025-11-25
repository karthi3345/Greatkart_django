from ctypes.wintypes import HACCEL
import http
from math import e
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from card.models import Card_item, Card
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q   #Q() → allows complex lookups (OR, AND)
# instead of this:
# from myapp.card.views import _card_id
# Wrong:




# do this:
from card.views import _card_id
from card.models import Card_item


# Create your views here.
def store(request, category_slug=None):

    category = None
    # sizes = ["S", "M", "L", "XL"]

    if category_slug is not None:
        # Fetch the category
        category = get_object_or_404(Category, slug=category_slug)
        # Filter products under that category
        products = Product.objects.filter(category=category, is_available=True) # filter needs key arguments
        paginator = Paginator(products, 2)  # Show 6 products per page
        page = request.GET.get('page')  # Get the page number from the request & capture url with the number
        paged_products = paginator.get_page(page)
    else:
        # Show all available products
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)  # Show 6 products per page
        page = request.GET.get('page')  # Get the page number from the request & capture url with the number
        paged_products = paginator.get_page(page)  # get the products for the requested page

    # Count products
    product_count = len(paged_products)



    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request,category_slug,product_slug):
    # Get product using both category slug and product slug
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,  # double underscore to follow ForeignKey
        slug=product_slug
    )
    in_cart = Card_item.objects.filter(
        card__card_id=_card_id(request), 
        product=single_product
       
    ).exists() #if it exist use exists method it will provude the boolean value
    # return HttpResponse("False")
    
    # print(in_cart)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'links': Category.objects.all(), # 👈 categories 
    }
    return render(request,'product_detail.html', context)


def search(request):
    if 'keyword' in request.GET: #get request having keyword or not
        keyword=request.GET['keyword'] # getting the keyword from the input field and storing in keyword variable
        if keyword:
            products=Product.objects.order_by('-created_date').filter(description__icontains=keyword) # icontains is used to search the keyword in description field
            products = Product.objects.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        )
            
            
        else:
            products=None
            product_count=0
        context={
            'products':products,    
            
        }       

    return render(request, 'store/store.html', context) 