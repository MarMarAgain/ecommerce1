from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineItemInline]

    readonly_fields = ('order_number', 'date_of_birth', 'grand_total',)

    # fieldsets should define fields within a section (can be nested)
    fields = ('order_number', 'full_name', 'email', 'phone_number',
              'postcode', 'street_address1', 'street_address2')

    list_display = ('order_number', 'date_of_birth', 'full_name')

    ordering = ('-date_of_birth',)

admin.site.register(Order, OrderAdmin)
