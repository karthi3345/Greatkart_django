from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Card, Card_item
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


# private function to get/create card ID
def _card_id(request):
    card = request.session.session_key
    if not card:
        card = request.session.create()
    return card


def add_card(request, product_id):
    product = Product.objects.get(id=product_id)

    # get or create the cart/card
    try:
        cart = Card.objects.get(card_id=_card_id(request))
    except Card.DoesNotExist:
        cart = Card.objects.create(card_id=_card_id(request))
        cart.save()

    # get or create the cart item
    try:
        cart_item = Card_item.objects.get(product=product, card=cart)
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except Card_item.DoesNotExist:
        cart_item = Card_item.objects.create(
            product=product,
            quantity=1,
            card=cart
        )
        cart_item.save()


   

    return redirect('card')

 # we going to get card and quantitiy 
def card(request, total=0, quantity=0,  tax=0 , grand_total=0,cart_items=None):

    try:
        cart=Card.objects.get(card_id=_card_id(request))
        cart_items=Card_item.objects.filter(card=cart, is_active=True)
        # want to caluclate aoal and all steps
        for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity) # total items im getting
            quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
    except Card.DoesNotExist:
        pass  # ignore if cart does not exist
        
    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total+tax,
        }
    return render(request, 'store/card.html', context)


def dec_card(request, product_id):
    cart = Card.objects.get(card_id=_card_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Card_item.objects.get(product=product, card=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1 #we should able to decrease quantity
        cart_item.save() # after that we have to save this 
    else:
        cart_item.delete() # else we have to delete this

    return redirect('card') # redirect to card page


def remove_card(request, product_id):
    cart = Card.objects.get(card_id=_card_id(request))  # get the cart using session card id
    #This is the filter condition.card_id is a field in your Card model._card_id(request) is presumably a custom function that returns the unique ID of the cart for this user/session.
    product = get_object_or_404(Product, id=product_id)
    cart_item = Card_item.objects.get(product=product, card=cart)
    cart_item.delete() # delete the cart item from the cart
    return redirect('card') # redirect to card page 