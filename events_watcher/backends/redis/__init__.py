import inspect
from datetime import datetime

from django.db.models import Model

from events_watcher.utils import load_class
from events_watcher import settings
from ..base import Backend

import redisco


class RedisBackend(Backend):
    filters = [
        (lambda instance: isinstance(instance, str), 'list_from_string'),
        (lambda instance: isinstance(instance, Model), 'list_from_instance'),
        (lambda instance: inspect.isclass(instance) and issubclass(instance, Model), 'list_from_class'),
    ]

    def __init__(self):
        super(RedisBackend, self).__init__()

        redisco.connection_setup(**settings.REDIS_CONNECTION)

        self.model = load_class(settings.REDIS_CONNECTION_CLASS)

    def add(self, key, instance, date=None):
        if not date:
            date = datetime.now()

        event = self.model(name=key,
                           reference=self.make_key_from_instance(instance),
                           date=date,
                           object_id=instance.pk)
        event.save()

        return event

    def list_from_string(self, string):
        return self.model.objects.filter(name=string)

    def list_from_instance(self, instance):
        return self.model.objects.filter(reference=self.make_key_from_instance(instance),
                                         object_id=instance.id)

    def list_from_class(self, klass):
        return self.model.objects.filter(reference=self.make_key_from_class(klass))

    def remove(self, instance):
        for event in self.list(instance):
            event.delete()

    def retrieve(self, name, instance):
        events = self.list(instance).filter(name=name)

        if len(events):
            return events[0]

        return False
