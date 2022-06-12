from datetime import timedelta

from django.db import models


class City(models.Model):
    name = models.CharField(max_length=40)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return self.name


class FlightRoute(models.Model):
    location = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="flight_routes"
    )
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.location.name} - {self.time}"


class FlightPrice(models.Model):
    economy = models.FloatField()
    economy_plus = models.FloatField()
    business = models.FloatField()
    first_class = models.FloatField()

    def __str__(self) -> str:
        return f"Prices for {self.flight.name}"


class Flight(models.Model):
    name = models.CharField(max_length=40)
    departure = models.OneToOneField(
        FlightRoute, on_delete=models.CASCADE, related_name="departure"
    )
    arrival = models.OneToOneField(
        FlightRoute, on_delete=models.CASCADE, related_name="arrival"
    )
    price = models.OneToOneField(
        FlightPrice, on_delete=models.CASCADE, related_name="flight"
    )

    def __str__(self) -> str:
        return self.name

    @property
    def trip(self) -> str:
        return f"{self.departure.location.name} TO {self.arrival.location.name}"

    @property
    def duration(self) -> timedelta:
        return self.arrival.time - self.departure.time
