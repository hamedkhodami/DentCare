from django.contrib import admin
from .models import (
    CartModel,
    CartItemModel,
    OrderModel,
    OrderItemModel,
    PaymentModel
)


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'is_submitted', 'submitted_at')
    list_filter = ('is_submitted',)
    search_fields = ('doctor__full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'case_item', 'price')
    list_filter = ('case_item__service',)
    search_fields = ('case_item__service__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'status', 'total_price', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('doctor__full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'case_item', 'price')
    list_filter = ('case_item__service',)
    search_fields = ('case_item__service__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'doctor', 'status', 'amount', 'paid_at')
    list_filter = ('status',)
    search_fields = ('doctor__full_name', 'paypal_transaction_id')
    readonly_fields = ('created_at', 'updated_at')