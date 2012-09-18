class Backend(object):
    filters = []

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
