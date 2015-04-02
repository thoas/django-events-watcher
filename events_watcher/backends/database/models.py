from __future__ import unicode_literals

from django.db import models

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey  # noqa

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Event(models.Model):
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(max_length=150)
    date = models.DateTimeField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType)

    class Meta:
        db_table = 'simple_events_event'
        unique_together = ('object_id', 'name', 'content_type')

    def __str__(self):
        return '%s for %s' % (self.name, self.content_object)
