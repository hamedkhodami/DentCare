from django.contrib import admin
from django.utils.html import format_html
from .models import User, UserProfileModel, PatientModel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_verified', 'last_login')
    list_filter = ('role', 'is_active', 'is_verified', 'country')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('token', 'last_login', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'role', 'expertise', 'country')
        }),
        ('Status', {
            'fields': ('is_active', 'is_admin', 'is_verified', 'token')
        }),
        ('Security', {
            'fields': ('password',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name()


@admin.register(UserProfileModel)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender', 'city', 'show_image')
    list_filter = ('gender', 'city')
    search_fields = ('user__email', 'phone_number', 'degree')
    ordering = ('-created_at',)

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.image.url)
        return "—"
    show_image.short_description = "Profile Image"


@admin.register(PatientModel)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_code', 'full_name', 'gender', 'age', 'created_by')
    list_filter = ('gender', 'created_by')
    search_fields = ('patient_code', 'full_name')
    ordering = ('-created_at',)

    readonly_fields = ('patient_code',)

    fieldsets = (
        (None, {
            'fields': ('patient_code', 'full_name', 'gender', 'age')
        }),
        ('Created Info', {
            'fields': ('created_by',)
        }),
    )
