from django.contrib import admin
from .models import PWD, TrafficViolation, RoadUser
from .forms import PWDForm

@admin.register(RoadUser)
class RoadUserAdmin(admin.ModelAdmin):  # Use default ModelAdmin
    list_display = ('name', 'number_plate', 'phone_number')
    search_fields = ('name', 'number_plate', 'phone_number')
    list_filter = ('number_plate',)
    ordering = ('name',)  # Add ordering by name

@admin.register(PWD)
class PWDAdmin(admin.ModelAdmin):  # Use default ModelAdmin
    form = PWDForm
    list_display = ('name', 'phone_number', 'mac_address', 'id_number')
    search_fields = ('name', 'phone_number', 'id_number')
    list_filter = ('id_number',)  # Add filter by ID number

    def mac_address(self, obj):
        return obj.mac_address
    mac_address.short_description = 'MAC Address'

@admin.register(TrafficViolation)
class TrafficViolationAdmin(admin.ModelAdmin):  # Use default ModelAdmin
    list_display = ('id', 'number_plate', 'verified', 'blacklisted', 'car_image')
    list_filter = ('verified', 'blacklisted')
    search_fields = ('number_plate',)
    ordering = ('-id',)  # Order by ID descending

