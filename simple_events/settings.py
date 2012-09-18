from django.conf import settings


BACKEND = getattr(settings,
                  'SIMPLE_EVENTS_BACKEND',
                  'simple_events.backends.database.DatabaseBackend')

DATABASE_CONNECTION_CLASS = getattr(settings,
                                    'SIMPLE_EVENTS_DATABASE_CONNECTION_CLASS',
                                    'simple_events.backends.database.models.Event')

REDIS_CONNECTION = getattr(settings,
                           'SIMPLE_EVENTS_REDIS_CONNECTION',
                           {'host': 'localhost', 'port': 6379, 'db': 0})

REDIS_CONNECTION_CLASS = getattr(settings,
                                 'SIMPLE_EVENTS_REDIS_CONNECTION_CLASS',
                                 'simple_events.backends.redis.models.Event')
