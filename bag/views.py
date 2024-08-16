from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, CalendarEvent

def view_bag(request):
    return render(request, 'bag.html')

def add_to_bag(request, item_id):
    """ Add the specified product and event to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    event_id = request.POST.get('event')  # Get the selected event ID
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Add the product and event to the bag
    bag[item_id] = event_id

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)

def remove_from_bag(request, item_id):
    """ Remove the specified product from the shopping bag """
    bag = request.session.get('bag', {})

    # Remove the item from the bag
    if item_id in bag:
        del bag[item_id]

    request.session['bag'] = bag
    return redirect('view_bag')