=======
Ytimer
=======

Purpose
-------
Ytimer is a Django app to schedule timers using database as storage.

Quick start
-----------

1. Add "ytimer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "ytimer",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("", include("ytimer.urls")),

3. Run ``python manage.py migrate`` to create the ytimer models.

4. Create a ytimer_handler modeule in your app. See ytimer_example for ytimer's usage.

5. POST http://127.0.0.1:8000/default_timer_handler/ to triger the timers.