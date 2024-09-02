import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(email):
    try:
        customer = stripe.Customer.create(email=email)
        return customer
    except stripe.error.StripeError as e:
        raise ValueError(e.user_message)
    except Exception as e:
        raise ValueError(str(e))

def attach_payment_method(customer_id, payment_method_id):
    try:
        # Attach the PaymentMethod to the Customer
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )
        # Update the Customer's default payment method
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                'default_payment_method': payment_method_id,
            }
        )
        return payment_method
    except stripe.error.StripeError as e:
        raise ValueError(e.user_message)
    except Exception as e:
        raise ValueError(str(e))
