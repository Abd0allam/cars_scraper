from django.contrib import admin
from .models import UsedCars, NewdCars

class UsedCarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'odo', 'image_url')

class NewdCarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_url')

admin.site.register(UsedCars, UsedCarsAdmin)
admin.site.register(NewdCars, NewdCarsAdmin)