from .base import Backend


class RedisBackend(Backend):
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
