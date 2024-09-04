from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe
from .stripe_func import attach_payment_method, create_customer
from products.models import CalendarEvent, Booking
from profiles.models import Profile
from .models import OrderLineItem, Order


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            payment_method_id = request.POST.get('payment_method_id')
            if not payment_method_id:
                messages.error(request, "Payment method is required.")
                return render(request, 'checkout/checkout.html', {'form': form})

            # Get the bag contents and total amount
            current_bag = bag_contents(request)
            total = current_bag['total']
            stripe_total = round(total * 100)

            # Create or retrieve customer
            try:
                stripe_customer_data = create_customer(form.cleaned_data['email'])
                stripe_customer_id = stripe_customer_data['id']
                attach_payment_method(stripe_customer_id, payment_method_id)
            except ValueError as e:
                messages.error(request, f"Error: {str(e)}")
                return render(request, 'checkout/checkout.html', {'form': form})

            try:
                # Create a PaymentIntent
                stripe.api_key = stripe_secret_key
                intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    payment_method=payment_method_id,
                    customer=stripe_customer_id,
                    currency=settings.STRIPE_CURRENCY,
                    metadata={'integration_check': 'accept_a_payment'},
                    confirm=True,
                    automatic_payment_methods={
                        'enabled': True,
                        'allow_redirects': 'never'
                    }
                )

                if intent.status == 'succeeded':
                    # Payment was successful
                    # Create the order and bookings
                    order = create_order(form.cleaned_data, current_bag, request.user)

                    # Create bookings for each event in the cart
                    for item in current_bag['bag_items']:
                        event = CalendarEvent.objects.get(id=item['event_id'])  # Get event by ID
                        Booking.objects.create(
                            user=request.user,
                            product=item['product'],
                            date_time=event.start_time  # Assuming `start_time` is the datetime for the booking
                        )

                    messages.success(request, "The payment has been successfully completed.")
                    return redirect('checkout_success')  # Redirect to a success page

                messages.error(request, "Payment failed. Please try again.")
                return render(request, 'checkout/checkout.html', {
                    'form': form,
                    'stripe_public_key': stripe_public_key,
                    'client_secret': intent.client_secret,
                    'bag_items': current_bag['bag_items'],
                    'total': total,
                })

            except stripe.error.StripeError as e:
                messages.error(request, f"Stripe error: {e.user_message}")
                return render(request, 'checkout/checkout.html', {'form': form})
            except Exception as e:
                messages.error(request, f"Unexpected error: {str(e)}")
                return render(request, 'checkout/checkout.html', {'form': form})

        return render(request, 'checkout/checkout.html', {'form': form})

    else:
        form = OrderForm()
        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)

        try:
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
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
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")
            return render(request, 'checkout/checkout.html', {'form': form})


def create_order(form_data, bag, user):
    """ Create an order instance based on the form and bag data """
    order = Order(
        user_profile=Profile.objects.get(user=user),
        full_name=form_data['full_name'],
        phone_number=form_data['phone_number'],
        email=form_data['email'],
        school_name=form_data['school_name'],
        grand_total=bag['total']
    )
    order.save()

    for item in bag['bag_items']:
        OrderLineItem.objects.create(
            order=order,
            product=item['product'],
            event=CalendarEvent.objects.get(id=item['event_id']),
            quantity=item['quantity']
        )

    return order

def checkout_success(request):
    """ A view to return the checkout success page """
    return render(request, 'checkout/checkout_success.html')