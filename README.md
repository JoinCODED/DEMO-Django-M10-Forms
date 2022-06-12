# Django Forms

Introduce students to forms and crispy forms.

## What are the objectives?

- Understand what forms are and how to use them
- Understand how to set up crispy forms

## Pre-requisites

1. Clone this repo.
2. Create a virtual environment.
3. Install the deps using `pip install -r requirements/dev.lock`.
4. Create an admin account using `python manage.py createsuperuser` and create some `flights`.

## Steps

### Create Form

1. Create a `forms.py` module inside the `flights` package.
2. Create a form for Flight like so:

   ```python
   from django import forms
   from flights.models import Flight

   class FlightForm(forms.ModelForm):
       class Meta:
           model = Flight
           fields = ["name", "departure", "arrival", "price"]
   ```

3. Add a view for our flight creation:

   ```python
   ...

   from flights.forms import FlightForm

   ...

   def create_flight(request):
       form = FlightForm()
       context = {
           "form": form,
       }
       return render(request, "create_flight.html", context)
   ```

4. Add our view to `urls.py`:

   ```python
   ...

   urlpatterns = [
       ...
       path("flights/", views.create_flight, name="create-flight"),
   ]
   ```

5. Add our `flights/templates/create_flight.html`:

   ```html
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta http-equiv="X-UA-Compatible" content="IE=edge" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Create Flight</title>
     </head>
     <body>
       {{ form }}
       <input type="submit" value="Add Flight" />
     </body>
   </html>
   ```

6. Explain that this just displays it, to actually get it working we have to wrap it in a `form` tag and add an action:

   ```html
   <form action="{% url 'create-flight' %}" method="POST">
     {% csrf_token %}
     <!-- prettier-ignore -->
     {{ form }}
     <input type="submit" value="Add flight" />
   </form>
   ```

   - Explain that `csrf_token` is to protect us against `Cross-Site Request Forgery`

7. We must actually handle the `POST` request now when the form is submitted, as follows:

   ```python
   from django.shortcuts import render, redirect

   ...

   def create_flight(request):
       form = FlightForm()
       if request.method == "POST":
           form = ModelNameForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect("flight-list")
       context = {
           "form": form,
       }
       return render(request, "create_flight.html", context)
   ```

   - Explain that the conditional `if request.method == "POST":` is `True` when the `form` is submitted. We redirect the user to the list of flights once we've created it, but we could have went anywhere. If the form is invalid, then we will keep showing the form.

8. Demonstrate this new piece of code by trying to create some flights.

### Update & Delete Views

#### Update View

1. Add our view for updating like so:

   ```python
   def update_flight(request, flight_id):
       flight = Flight.objects.get(id=flight_id)
       form = FlightForm(instance=flight)
       if request.method == "POST":
           form = FlightForm(request.POST, instance=flight)
           if form.is_valid():
               form.save()
               return redirect("flight-detail", flight_id=flight_id)
       context = {
           "flight": flight,
           "form": form,
       }
       return render(request, 'update_flight.html', context)
   ```

   - This is extremely similar to our create view, however, this time we are redirecting back to the detail page of our flight, and in our context we've added flight.

2. Add our `update_flight` to our `urls.py` and add the name `update-flight`.
3. In our templates we are `update_flight.html`:

   ```html
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta http-equiv="X-UA-Compatible" content="IE=edge" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Update Flight</title>
     </head>
     <body>
       <form
         action="{% url 'update-flight' flight_id=flight.id %}"
         method="POST"
       >
         {% csrf_token %}
         <!-- prettier-ignore -->
         {{ form }}
         <input type="submit" value="Save Flight" />
       </form>
     </body>
   </html>
   ```

   - Explain how it is still a `POST` method, and that the action is a bit different. The `csrf_token` does the same thing as it did in our create view. Finally, our submit button text is different.

4. Update some flights and show them how it works.

#### Delete View

1. Add our `delete` view in `views.py`:

   ```python
   def delete_flight(request, flight_id):
       try:
           flight = Flight.objects.get(id=flight_id)
       except Flight.DoesNotExist:
           raise Http404("flight does not exist")

       flight.delete()
       return redirect("flight-list")
   ```

2. Add our `delete` view to our `urls.py` with the name `delete-flight`:

   ```python
   ...

   urlpatterns = [
      ...
      path("flights/<int:flight_id>", views.delete_flight, name="delete-flight"),
   ]
   ```

3. Add a `delete` anchor tag to our `flight_list.html` template like so:

   ```html
   ...
   <p>Duration: {{ flight.duration }}</p>
   <a href="{% url 'delete-flight' flight_id=flight.id %}">Delete Flight</a>
   ...
   ```
