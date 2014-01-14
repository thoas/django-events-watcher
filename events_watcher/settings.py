from django.conf import settings


BACKEND = getattr(settings,
                  'EVENTS_WATCHER_BACKEND',
                  'events_watcher.backends.database.DatabaseBackend')

DATABASE_CONNECTION_CLASS = getattr(settings,
                                    'EVENTS_WATCHER_DATABASE_CONNECTION_CLASS',
                                    'events_watcher.backends.database.models.Event')
