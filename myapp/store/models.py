from itertools import product
from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    img=models.ImageField(upload_to='photos/products',blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE) # whenever we delete category the product attached to the category also delete
    created_date=models.DateField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='store'
        db_table = 'store'


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name
    
    
    
 # color & sizes
 
class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)

    def sizes(self):
        return self.filter(variation_category='size', is_active=True)   
    
    
# store/models.py
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100,
        choices=(('color','color'), ('size','size'))
    )
    variation_value = models.CharField(max_length=100)  # ✅ correct spelling
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
   