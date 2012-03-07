====================
django-simple-events
====================

Add new events for auth.users::

    In [5]: user = User.objects.create_user('newbie', 'newbie@example.com', '$ecret')

    In [6]: Event.objects.add('subscription', user)
    Out[6]: <Event: subscription for newbie>

    In [7]: Event.objects.add('subscription', user, date=user.date_joined)
    Out[7]: <Event: subscription for newbie>

List all events for auth.users::

    In [12]: Event.objects.list(user)
    Out[12]: [<Event: subscription for newbie>, <Event: subscription for newbie>]

    In [13]: Event.objects.add('last_login', user, date=user.last_login)
    Out[13]: <Event: last_login for newbie>

    In [14]: Event.objects.list('last_login')
    Out[14]: [<Event: last_login for newbie>]

Retrieve only one event for a specific event name and auth.users::

    In [16]: Event.objects.retrieve('last_login', user)
    Out[16]: <Event: last_login for newbie>

Remove all events with a specific event name::

    In [17]: Event.objects.remove('last_login')

Installation
------------

`python setup.py install`

OR

put the ``simple_events`` folder on your python-path

Add ``simple_events`` to your `INSTALLED_APPS`.

Roadmap
-------

Currently only databases shipped with the default Django ORM is supported and
the API is very simple.

Custom backends could be done to store results in databases like: ``redis`` or
``MongoDB``.
