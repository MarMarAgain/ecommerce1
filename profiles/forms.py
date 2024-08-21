# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')
    full_name = forms.CharField(max_length=100, required=True, help_text='Required.')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()  # Save the user instance first
            Profile.objects.create(user=user)
        return user

class ProfileForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields = ['profile_picture','school_details', 'students_info',]
       widgets = {
           'school_details': forms.Textarea(attrs={'placeholder': "Please enter your school's details here"}),
           'students_info': forms.Textarea(attrs={
            'placeholder':
            'Please enter the cycle and level you primarily teach here. You can also add any other information.'}),
        }
