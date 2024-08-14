from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='workshop_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]