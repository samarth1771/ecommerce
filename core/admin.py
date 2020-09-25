from django.contrib import admin
from .models import *


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'ordered_date',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'payment',
                    'coupon']
    list_filter = ['ordered',
                   'ordered_date',
                   'being_delivered',
                   'received', 'refund_requested',
                   'refund_granted']

    list_display_links = ['billing_address',
                          'payment',
                          'coupon']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
