from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.

class Category (models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug= models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank= True)
    category_img=models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name=_('category')
        verbose_name_plural='categories'
        db_table = 'categories'


# 1️⃣ The code
# def get_url(self):
#     return reverse('products_by_category', args=[self.slug])

# 2️⃣ Explanation

# def get_url(self):

# This is a method of a model (usually inside Category or Product).

# self → refers to the current instance of the model.

# reverse()

# Django built-in function that returns the URL for a given view name.

# It is the programmatic way to get URLs instead of hardcoding them.

# 'products_by_category'

# This is the name of the URL pattern in urls.py:

# path('store/<slug:category_slug>/', views.store, name='products_by_category')


# args=[self.slug]

# Passes the slug of the category as a parameter to the URL.

# self.slug → the slug attribute of the current instance.

# 3️⃣ How it works

# Suppose you have a category object:

# category = Category.objects.get(id=1)
# category.slug  # 'shirts'


    def __str__(self):
       return self.category_name
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

