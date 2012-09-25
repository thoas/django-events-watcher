from redisco import models

from ..mixins import EventMixin


class Event(EventMixin, models.Model):
    name = models.Attribute()
    object_id = models.IntegerField()
    reference = models.Attribute()
    date = models.DateTimeField(required=False)

    @property
    def content_object(self):
        return self._get_model_class().objects.get(pk=self.object_id)

    @property
    def content_type(self):
        from django.contrib.contenttypes.models import ContentType

        return ContentType.objects.get_for_model(self._get_model_class())

    def _get_model_class(self):
        from django.db import models

        return models.get_model(*self.reference.split('.'))
