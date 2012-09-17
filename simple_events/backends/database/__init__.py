from django.core.exceptions import ImproperlyConfigured

from ..base import Backend

from simple_events import settings
from simple_events.utils import load_class


class DatabaseBackend(Backend):
    def __init__(self):
        self.model = load_class(settings.DATABASE_CONNECTION_CLASS)

        if not self.model._meta.installed:
            raise ImproperlyConfigured(
                "The simple_events.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS settings.")

    def add(self, name, instance, date=None):
        return self.model.objects.add(name, instance, date=date)

    def list(self, instance):
        return list(self.model.objects.list(instance))

    def remove(self, instance):
        return self.model.objects.remove(instance)

    def retrieve(self, name, instance):
        return self.model.objects.retrieve(name, instance)
