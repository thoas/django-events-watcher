import inspect

from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType


class EventManager(models.Manager):
    def add(self, name, instance, date=None):
        if not date:
            date = datetime.now()

        content_type = ContentType.objects.get_for_model(instance)

        event = self.create(object_id=instance.pk, \
                            name=name, \
                            date=date, \
                            content_type=content_type)

        return event

    def list(self, instance):
        if isinstance(instance, str):
            qs = self.filter(name=instance)
        elif isinstance(instance, models.Model):
            qs = self.filter(content_type=ContentType.objects.get_for_model(instance), \
                             object_id=instance.pk)
        elif inspect.isclass(instance) and issubclass(instance, models.Model):
            qs = self.filter(content_type=ContentType.objects.get_for_model(instance))
        else:
            qs = self.none()

        return qs

    def remove(self, instance):
        return self.list(instance).delete()

    def retrieve(self, name, instance):
        return self.get(content_type=ContentType.objects.get_for_model(instance), \
                        object_id=instance.pk, name=name)
