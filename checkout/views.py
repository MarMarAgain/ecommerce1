from django.shortcuts import render
from .forms import OrderForm

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or handle payment processing here
    else:
        form = OrderForm()

    context = {
        'form': form,
        'stripe_public_key': 'pk_test_51PT97iJqhZ1fbf5raRgusRdwBQ6RQwsBzuraaJm92yb52sDMApayeju6LPsJrMQEJSXp4U0e08o7KkECD3p6AGGg009LgKSycm',
        'client_secret': 'test client secret',  # Replace this with a real client secret from a PaymentIntent
    }

    return render(request, 'checkout/checkout.html', context)




