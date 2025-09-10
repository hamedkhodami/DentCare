from django.contrib import admin
from .models import (
    CaseModel,
    CaseToothModel,
    CaseItemModel,
    CaseItemOptionModel,
    MirrorCopyModel,
    CaseAttachment
)


@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'patient__full_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CaseToothModel)
class CaseToothAdmin(admin.ModelAdmin):
    list_display = ('case', 'tooth_number', 'tooth_position')
    list_filter = ('tooth__position',)
    search_fields = ('case__title', 'tooth__number')
    readonly_fields = ('created_at', 'updated_at')

    def tooth_number(self, obj):
        return obj.tooth.number
    tooth_number.short_description = "Tooth Number"

    def tooth_position(self, obj):
        return obj.tooth.get_position_display()
    tooth_position.short_description = "Position"


@admin.register(CaseItemModel)
class CaseItemAdmin(admin.ModelAdmin):
    list_display = ('service', 'case_tooth', 'material', 'status', 'price')
    list_filter = ('status', 'service', 'material')
    search_fields = (
        'service__name',
        'case_tooth__tooth__number',
        'case_tooth__case__title'
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CaseItemOptionModel)
class CaseItemOptionAdmin(admin.ModelAdmin):
    list_display = ('case_item', 'option', 'value')
    list_filter = ('option__input_type', 'option__level')
    search_fields = ('option__label', 'value')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MirrorCopyModel)
class MirrorCopyAdmin(admin.ModelAdmin):
    list_display = ('case', 'source_tooth_display', 'target_tooth_display', 'copy_type')
    list_filter = ('copy_type',)
    search_fields = (
        'case__title',
        'source_tooth__tooth__number',
        'target_tooth__tooth__number'
    )
    readonly_fields = ('created_at', 'updated_at')

    def source_tooth_display(self, obj):
        return obj.source_tooth.tooth.number
    source_tooth_display.short_description = "Source Tooth"

    def target_tooth_display(self, obj):
        return obj.target_tooth.tooth.number
    target_tooth_display.short_description = "Target Tooth"


@admin.register(CaseAttachment)
class CaseAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'linked_item', 'file_type', 'uploaded_by', 'is_private', 'created_at')
    list_filter = ('file_type', 'is_private')
    search_fields = ('description', 'case__title', 'linked_item__service__name', 'uploaded_by__full_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

