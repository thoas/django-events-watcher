import inspect

from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from ..base import Backend

from events_watcher import settings
from events_watcher.utils import load_class

from datetime import datetime


class DatabaseBackend(Backend):
    filters = [
        (lambda instance: isinstance(instance, str), 'list_from_string'),
        (lambda instance: isinstance(instance, Model), 'list_from_instance'),
        (lambda instance: inspect.isclass(instance) and issubclass(instance, Model), 'list_from_class'),
    ]

    def __init__(self):
        super(DatabaseBackend, self).__init__()

        self.model = load_class(settings.DATABASE_CONNECTION_CLASS)

        if not self.model._meta.installed:
            raise ImproperlyConfigured(
                "The events_watcher.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS settings.")

    def add(self, name, instance, date=None):
        if not date:
            date = datetime.now()

        content_type = ContentType.objects.get_for_model(instance)

        event = self.model.objects.create(object_id=instance.pk,
                                          name=name,
                                          date=date,
                                          content_type=content_type)

        return event

    def list_from_string(self, string):
        return self.model.objects.filter(name=string)

    def list_from_instance(self, instance):
        return self.model.objects.filter(content_type=ContentType.objects.get_for_model(instance),
                                         object_id=instance.pk)

    def list_from_class(self, klass):
        return self.model.objects.filter(content_type=ContentType.objects.get_for_model(klass))

    def remove(self, instance):
        return self.list(instance).delete()

    def retrieve(self, name, instance):
        try:
            return self.model.objects.get(content_type=ContentType.objects.get_for_model(instance),
                                          object_id=instance.pk, name=name)
        except self.model.DoesNotExist:
            return False
