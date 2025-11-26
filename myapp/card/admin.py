from django.contrib import admin

# Register your models here.

from .models import Card 
from .models import Card_item



from django.contrib import admin
from .models import Card, Card_item

class CardItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'card', 'quantity', 'is_active')

admin.site.register(Card)
admin.site.register(Card_item, CardItemAdmin)
