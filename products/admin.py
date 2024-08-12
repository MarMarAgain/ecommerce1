from django.contrib import admin
from .models import Product, Category, CalendarEvent

class CalendarEventInline(admin.TabularInline):
    model = CalendarEvent
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [CalendarEventInline]
    list_display = ('name', 'category')

# Registered models with Django admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(CalendarEvent)
