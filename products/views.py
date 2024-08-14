# products/views.py
from django.shortcuts import render
from .models import Product, CalendarEvent
from django.shortcuts import get_object_or_404, redirect



def product_list(request):
    products = Product.objects.prefetch_related('events').all()
    return render(request, 'products/workshop_list.html', {'products': products})


def add_to_cart(request, product_id):
    if request.method == "POST":
        event_id = request.POST.get('event')
        event = get_object_or_404(CalendarEvent, id=event_id)
        # Add logic to add the event to the user's cart
        # e.g., request.session['cart'].append(event)
        return redirect('cart_view')  # Redirect to the cart page or another appropriate page

    return redirect('product_list')  # Redirect to product list if not a POST request
