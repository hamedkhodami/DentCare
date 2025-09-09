from django.contrib import admin
from .models import ToothChartModel, ToothModel, OcclusionLinkModel


@admin.register(ToothChartModel)
class ToothChartAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_at', 'updated_at')
    search_fields = ('patient__full_name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ToothModel)
class ToothAdmin(admin.ModelAdmin):
    list_display = ('number', 'chart', 'status', 'position', 'color_preview')
    list_filter = ('status', 'position')
    search_fields = ('number', 'chart__patient__full_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('number',)

    def color_preview(self, obj):
        if obj.color_code:
            return f"{obj.color_code}"
        return "—"
    color_preview.short_description = "Color Code"


@admin.register(OcclusionLinkModel)
class OcclusionLinkAdmin(admin.ModelAdmin):
    list_display = ('source_tooth', 'target_tooth', 'relation', 'chart')
    list_filter = ('relation',)
    search_fields = (
        'source_tooth__number',
        'target_tooth__number',
        'chart__patient__full_name'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('source_tooth__number',)
