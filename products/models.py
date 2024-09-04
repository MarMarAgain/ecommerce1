from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length=250)
    friendly_name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True ,on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)
    description = models.TextField()
    duration = models.CharField(max_length=50, default='90 minutes')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='events')
    start_time = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Event for {self.product.name} on {self.start_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} booked {self.product.name} at {self.date_time}"