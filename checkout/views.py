from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings
import stripe
from .stripe_func import attach_payment_method, create_customer

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Don't save the form immediately. Instead, save after payment confirmation.
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
                    messages.success(request, "The payment has been successfully completed.")
                    return redirect('checkout_success')  # Redirect to a success page

                # If payment intent does not succeed
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

        # If form is invalid
        return render(request, 'checkout/checkout.html', {'form': form})

    else:
        form = OrderForm()

        # Get the bag contents and total amount for the initial view rendering
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



def checkout_success(request):
    """ A view to return the checkout success page """
    return render(request, 'checkout/checkout_success.html')