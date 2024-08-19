from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Don't save the form immediately. Instead, save after payment confirmation.

            # Get the bag contents and total amount
            current_bag = bag_contents(request)
            total = current_bag['total']
            stripe_total = round(total * 100)

            # Create a PaymentIntent
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                metadata={'integration_check': 'accept_a_payment'},
            )

            return render(request, 'checkout/checkout.html', {
                'form': form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
            })
    else:
        form = OrderForm()

        # Get the bag contents and total amount for the initial view rendering
        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)

        # Create a PaymentIntent for initial page load
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='eur',
            metadata={'integration_check': 'accept_a_payment'},
        )

    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bag_items': current_bag['bag_items'],
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)
