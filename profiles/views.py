from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import OrderLineItem
from .models import Profile
from products.models import Product
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """ Display the user's profile. """
    context = {}  # Add any necessary context data here
    return render(request, 'profiles/profile.html', context)



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile')  # Redirect to profile page after successful signup
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()  # This will save both User and Profile due to form's save method
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Failed to authenticate. Please try logging in.')
            return redirect('signup')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')  # Redirect to profile page after login


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile details have been saved.')
            return redirect('edit_profile')  # Redirect after successful form submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    booked_workshops = OrderLineItem.objects.filter(user=request.user).select_related('product')

    context = {
        'profile': profile,
        'form': form,
        'booked_workshops': booked_workshops,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def cancel_workshop(request, workshop_id):
    workshop = get_object_or_404(Product, pk=workshop_id)
    user = request.user

    # Find the corresponding OrderLineItem
    booked_workshop = get_object_or_404(OrderLineItem, user=user, product=workshop)

    # Remove the workshop from the user's booked workshops
    user.profile.booked_workshops.remove(workshop)

    # Delete the OrderLineItem instance
    booked_workshop.delete()

    messages.success(request, f'You have successfully canceled the workshop: {workshop.name}.')
    return redirect('profile')


def logout_view(request):
    logout(request)
    return redirect('login')
