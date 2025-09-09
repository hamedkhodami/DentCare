from django.contrib import admin
from .models import (
    SurchargeModel,
    PriceListModel,
    ServicePriceModel,
    QuoteRequestModel,
    QuoteItemModel,
    CaseSurchargeModel
)


@admin.register(SurchargeModel)
class SurchargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'amount', 'active')
    list_filter = ('type', 'active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PriceListModel)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'valid_from', 'valid_until')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServicePriceModel)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('price_list', 'service', 'material', 'scope', 'amount')
    list_filter = ('scope', 'price_list', 'service', 'material')
    search_fields = ('service__name', 'material__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QuoteRequestModel)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('case', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('case__title', 'case__patient__full_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QuoteItemModel)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('quote', 'service', 'material', 'suggested_price')
    list_filter = ('service', 'material')
    search_fields = ('service__name', 'material__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CaseSurchargeModel)
class CaseSurchargeAdmin(admin.ModelAdmin):
    list_display = ('case', 'surcharge', 'amount')
    list_filter = ('surcharge',)
    search_fields = ('case__title', 'surcharge__name')
    readonly_fields = ('created_at', 'updated_at')