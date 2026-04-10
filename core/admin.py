from django.contrib import admin
from .models import UserProfile, TransporterProfile, Requirement, Bid

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'contact_number')
    search_fields = ('user__username', 'contact_number')

@admin.register(TransporterProfile)
class TransporterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'transporter_name', 'vehicle_number')
    search_fields = ('transporter_name', 'vehicle_number')

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('source_city', 'destination_city', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('source_city', 'destination_city')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'transporter', 'amount', 'created_at')
    list_filter = ('created_at',)
