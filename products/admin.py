from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from .models import Product, Category, CalendarEvent

# Custom form to customize date and time widgets
class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['product', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
                time_attrs={'type': 'time'}
            ),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CalendarEventInline(admin.TabularInline):
    model = CalendarEvent
    form = CalendarEventForm
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [CalendarEventInline]
    list_display = ('name', 'category')


# Registered models with Django admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, )
