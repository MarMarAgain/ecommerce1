from django.contrib.auth.models import User
from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    school_details = models.TextField(blank=True)
    students_info = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    booked_workshops = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

