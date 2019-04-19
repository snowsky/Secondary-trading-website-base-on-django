from django.contrib import admin
from order.models import OrderStatusAndBillStatus
# Register your models here.


@admin.register(OrderStatusAndBillStatus)
class OrderStatusBillStatusAdmin(admin.ModelAdmin):
    list_display = ['status_number', 'status_content']