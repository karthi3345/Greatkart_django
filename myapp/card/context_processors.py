# card/context_processors.py
from .models import Card_item, Card
from .views import _card_id  # <- adjust if _card_id is in utils.py

def counter(request):
    total_items = 0

    if request.path.startswith('/admin'):
        return {}

    try:
        cart = Card.objects.get(card_id=_card_id(request))
        cart_items = Card_item.objects.filter(card=cart)  # get all items in the cart

        for item in cart_items:
            total_items += item.quantity  # sum quantity

    except Card.DoesNotExist:
        total_items = 0

    return {'counter': total_items}
