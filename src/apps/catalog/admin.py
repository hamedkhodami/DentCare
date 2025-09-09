from django.contrib import admin
from .models import (
    ServiceCategoryModel,
    ServiceModel,
    MaterialModel,
    ServiceMaterialModel,
    OptionGroupModel,
    OptionModel
)


@admin.register(ServiceCategoryModel)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ui_color', 'icon')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'pricing_type', 'form_type', 'is_per_tooth', 'active')
    list_filter = ('pricing_type', 'form_type', 'active', 'category')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(MaterialModel)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'active')
    list_filter = ('type', 'active')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ServiceMaterialModel)
class ServiceMaterialAdmin(admin.ModelAdmin):
    list_display = ('service', 'material', 'is_default')
    list_filter = ('is_default', 'service', 'material')
    search_fields = ('service__name', 'material__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OptionGroupModel)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OptionModel)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('label', 'group', 'input_type', 'level', 'required', 'active')
    list_filter = ('input_type', 'level', 'required', 'active', 'group')
    search_fields = ('label', 'group__name')
    readonly_fields = ('created_at', 'updated_at')