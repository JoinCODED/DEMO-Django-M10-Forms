from django.http import Http404
from django.shortcuts import render

from flights.models import Flight


def get_flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("could not find flight")

    context = {
        "flight": {
            "id": flight_id,
            "name": flight.name,
            "trip": flight.trip,
            "duration": flight.duration,
            "prices": flight.price,
        },
    }

    return render(request, "flight_detail.html", context)


def get_flights(request):
    flights = Flight.objects.all().iterator()

    context = {
        "flights": [
            {
                "id": flight.id,
                "name": flight.name,
                "trip": flight.trip,
                "duration": flight.duration,
            }
            for flight in flights
        ]
    }

    return render(request, "flight_list.html", context)
