from django.conf import settings


REDIS_PREFIX = getattr(settings, 'SIMPLE_EVENTS_REDIS_PREFIX',
                       getattr(settings, 'SIMPLE_EVENTS_PREFIX', 'simple_events:'))

BACKEND = getattr(settings,
                  'SIMPLE_EVENTS_BACKEND',
                  'simple_events.backends.database.DatabaseBackend')

DATABASE_CONNECTION_CLASS = getattr(settings,
                                    'SIMPLE_EVENTS_DATABASE_CONNECTION_CLASS',
                                    'simple_events.backends.database.models.Event')

REDIS_CONNECTION_CLASS = getattr(settings,
                                 'SIMPLE_EVENTS_REDIS_CONNECTION',
                                 'redis.client.Redis')
