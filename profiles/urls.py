from django.urls import path
from django.conf import settings
from .views import CustomLoginView, SignUpView, Profile, logout_view, cancel_workshop
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]