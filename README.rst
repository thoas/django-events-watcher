=====================
django-events-watcher
=====================

Add new events for auth.users::

    In [4]: from events_watcher.bridge import backend as events
    In [5]: user = User.objects.create_user('newbie', 'newbie@example.com', '$ecret')

    In [6]: events.add('subscription', user)
    Out[6]: <Event: subscription for newbie>

    In [7]: events.add('subscription', user, date=user.date_joined)
    Out[7]: <Event: subscription for newbie>

List all events for auth.users::

    In [12]: events.list(user)
    Out[12]: [<Event: subscription for newbie>, <Event: subscription for newbie>]

    In [13]: events.add('last_login', user, date=user.last_login)
    Out[13]: <Event: last_login for newbie>

    In [14]: events.list('last_login')
    Out[14]: [<Event: last_login for newbie>]

Retrieve only one event for a specific event name and auth.users::

    In [16]: events.retrieve('last_login', user)
    Out[16]: <Event: last_login for newbie>

Remove all events with a specific event name::

    In [17]: events.remove('last_login')

Installation
------------

`python setup.py install`

OR

put the ``events_watcher`` folder on your python-path

Add ``events_watcher.backends.database`` to your `INSTALLED_APPS` if you want to
use the RDMS backend connector with the Django ORM.

Roadmap
-------

Currently only databases shipped with the default Django ORM is supported and
the API is very simple.

Custom backends could be done to store results in NoSQL databases like: ``redis`` or
``MongoDB``.

Notes
-----

``events_watcher`` uses a ``load_class`` helper in its ``utils`` module which can be found at `django-shop <https://github.com/divio/django-shop/blob/master/shop/util/loader.py>`_.
