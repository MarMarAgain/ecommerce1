from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout-success/', views.checkout_success, name='checkout_success'),
]