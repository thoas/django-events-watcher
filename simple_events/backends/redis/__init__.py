import inspect
from datetime import datetime

from django.db import models as django_models

from simple_events.utils import load_class
from simple_events import settings
from ..base import Backend


class RedisBackend(Backend):
    def __init__(self):
        import redisco
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

    def list(self, instance):
        from redisco.containers import Set

        if isinstance(instance, str):
            return self.model.objects.filter(name=instance)
        elif isinstance(instance, django_models.Model):
            return self.model.objects.filter(reference=self.make_key_from_instance(instance), object_id=instance.id)
        elif inspect.isclass(instance) and issubclass(instance, django_models.Model):
            return self.model.objects.filter(reference=self.make_key_from_class(instance))

        return Set(key=instance)

    def remove(self, instance):
        for event in self.list(instance):
            event.delete()

    def retrieve(self, name, instance):
        events = self.list(instance).filter(name=name)

        if len(events):
            return events[0]

        return False
