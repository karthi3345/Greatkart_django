from django.contrib import admin

# Register your models here.

from .models import Card 
from .models import Card_item

admin.site.register(Card)
admin.site.register(Card_item)