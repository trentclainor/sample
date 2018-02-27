from django.contrib import admin

from .models import City, Country, Industry, Location, Role, State

admin.site.register(Industry)
admin.site.register(Role)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Location)
