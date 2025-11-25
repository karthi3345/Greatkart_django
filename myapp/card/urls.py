from django.urls import path
from . import views

urlpatterns = [
    path ('', views.card , name='card'),
    path('add_card/<int:product_id>/', views.add_card, name='add_card'),
    path('dec_card/<int:product_id>/', views.dec_card, name='dec_card'),
    path('remove_card/<int:product_id>/', views.remove_card, name='remove_card'),
]
