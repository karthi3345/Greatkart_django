from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):

    category = None

    if category_slug is not None:
        # Fetch the category
        category = get_object_or_404(Category, slug=category_slug)
        # Filter products under that category
        products = Product.objects.filter(category=category, is_available=True) # filter needs key arguments
    else:
        # Show all available products
        products = Product.objects.filter(is_available=True)

    # Count products
   
    product_count = products.count()

    context = {
        'products': products,
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

    context = {
        'single_product': single_product
    }
    return render(request,'product_detail.html', context)
