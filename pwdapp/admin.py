from django.contrib import admin
from .models import PWD, TrafficViolation, RoadUser
from .forms import PWDForm

class CustomAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('pwdapp/bo.css',)  # Link your custom CSS here
        }

@admin.register(RoadUser)
class RoadUserAdmin(CustomAdmin):
    list_display = ('name', 'number_plate', 'phone_number')
    search_fields = ('name', 'number_plate', 'phone_number')
    list_filter = ('number_plate',)

@admin.register(PWD)
class PWDAdmin(CustomAdmin):
    form = PWDForm
    list_display = ('name', 'phone_number', 'mac_address', 'id_number')
    search_fields = ('name', 'phone_number', 'id_number')

    def mac_address(self, obj):
        return obj.mac_address
    mac_address.short_description = 'MAC Address'

@admin.register(TrafficViolation)
class TrafficViolationAdmin(CustomAdmin):
    list_display = ('id', 'number_plate', 'verified', 'blacklisted', 'car_image')
    list_filter = ('verified', 'blacklisted')
    search_fields = ('number_plate',)

