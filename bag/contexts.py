from decimal import Decimal

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0

    # Assuming each item has a 'price' and 'quantity' property.
    for item in request.session.get('bag', []):
        product = item['product']
        quantity = item['quantity']
        price = Decimal(product.price)
        total += price * quantity
        product_count += quantity
        bag_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': price * quantity,
        })

    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
