from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product, CalendarEvent

def bag_contents(request):
    bag_items = []
    total = 0

    # Assume the bag structure is {product_id: event_id}
    bag = request.session.get('bag', {})

    for product_id, event_id in bag.items():
        product = get_object_or_404(Product, pk=product_id)
        event = get_object_or_404(CalendarEvent, pk=event_id)  # Use CalendarEvent here
        price = Decimal(product.price)
        total += price

        bag_items.append({
            'product': product,
            'event': event,
            'price': price,
        })

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return context
