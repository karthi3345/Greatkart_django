from django.db import models
from store.models import Product
from django.utils.translation import gettext as _

# Create your models here.
class Card(models.Model):
    card_id=models.CharField(primary_key=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.card_id

class Card_item(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # FIXED
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
    
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.card.card_id}"


