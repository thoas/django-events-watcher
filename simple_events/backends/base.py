class Backend(object):
    def add(self, key, instance, date=None):
        """
        Add new event to the backend store and return the value.
        """
        raise NotImplementedError

    def list(self, instance):
        """
        Retrieve a list of events given an instance
        """
        raise NotImplementedError

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
        return u'%s.%s' % (klass._meta.app_label,
                           klass.__name__)

    def make_key_from_instance(self, instance):
        return u'%s.%s' % (instance._meta.app_label,
                           instance.__class__.__name__)

    def make_key_id_from_instance(self, instance):
        return u'%s:%s' % (self.make_key_from_instance(instance),
                           instance.pk)
