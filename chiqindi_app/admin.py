from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WasteReport, Notification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'role', 'phone', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumot', {'fields': ('role', 'phone', 'is_authority_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumot', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone')}),
    )


@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ['pk', 'citizen', 'waste_type', 'size', 'status', 'viloyat', 'tuman', 'created_at']
    list_filter = ['status', 'waste_type', 'size', 'viloyat']
    search_fields = ['citizen__username', 'tuman', 'address', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'message', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['recipient__username', 'message']
