from django.shortcuts import render
from .forms import OrderForm


def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page
    else:
        form = OrderForm()

    return render(request, 'checkout/checkout.html', {'form': form})



