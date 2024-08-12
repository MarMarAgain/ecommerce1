from django.db import models

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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Event for {self.product.name} on {self.start_time}"