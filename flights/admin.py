from django.contrib import admin

from flights import models

to_register = [
    models.City,
    models.FlightPrice,
    models.FlightRoute,
    models.Flight,
]

admin.site.register(to_register)
