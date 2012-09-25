from collections import defaultdict

from django.db.models.signals import post_save, pre_save


class Backend(object):
    filters = []

    def __init__(self):
        self.purge()

    def purge(self):
        self._callbacks = defaultdict(list)
        self._initial_data = {}

    def add(self, key, instance, date=None):
        """
        Add new event to the backend store and return the value.
        """
        raise NotImplementedError

    def list(self, instance):
        """
        Retrieve a list of events given an instance
        """
        for condition, method in self.filters:
            if condition(instance) and hasattr(self, method):
                return getattr(self, method)(instance)

        return []

    def remove(self, instance):
        """
        Remove all events from the backend store givent an instance
        """
        raise NotImplementedError

    def retrieve(self, name, instance):
        """
        Retrieve events from the backend store given a name and an instance.
        """
        raise NotImplementedError

    def make_key_from_class(self, klass):
        """
        Make a formatted key from a class
        """
        return u'%s.%s' % (klass._meta.app_label,
                           klass.__name__)

    def make_key_from_instance(self, instance):
        """
        Make a formatted key from an instance
        """
        return u'%s.%s' % (instance._meta.app_label,
                           instance.__class__.__name__)

    def make_key_id_from_instance(self, instance):
        """
        Make a formatted key with an id from an instance
        """
        return u'%s:%s' % (self.make_key_from_instance(instance),
                           instance.pk)

    def watch(self, klass, key, condition, callback=None):
        pre_save.connect(self._on_pre_save, sender=klass)
        post_save.connect(self._on_post_save, sender=klass)

        self._callbacks[klass].append((key, condition, callback))

    def _on_post_save(self, sender, instance, **kwargs):
        klass = instance.__class__
        identifier = self._make_identifier(instance)

        created = kwargs.get('created')

        if klass in self._callbacks and (identifier in self._initial_data[klass] or created):
            initial_data = self._initial_data[klass].get(identifier, {})

            for key, condition, callback in self._callbacks[klass]:
                if condition(initial_data, instance, created):
                    event = self.add(key, instance)

                    if callback:
                        callback(event,
                                 initial_data=initial_data,
                                 instance=instance,
                                 created=created)

    def _on_pre_save(self, sender, instance, **kwargs):
        klass = instance.__class__

        if klass in self._callbacks:
            if not klass in self._initial_data:
                self._initial_data[klass] = {}

            if instance.pk:
                previous_instance = klass.objects.get(pk=instance.pk)

                identifier = self._make_identifier(instance)

                self._initial_data[klass][identifier] = dict(previous_instance.__dict__)

    def _make_identifier(self, instance):
        return self.make_key_id_from_instance(instance) \
            if instance.pk else id(instance)
