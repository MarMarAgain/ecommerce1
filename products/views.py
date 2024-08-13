from django.shortcuts import render, get_object_or_404
from .models import Product

def workshop_list(request):
    workshops = Product.objects.all()  # Adjust this query if you have specific criteria for workshops
    return render(request, 'products/workshop_list.html', {'workshops': workshops})

def workshop_detail(request, id):
    workshop = get_object_or_404(Product, id=id)
    return render(request, 'products/workshop_detail.html', {'workshop': workshop})
