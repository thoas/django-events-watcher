from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from ..mixins import EventMixin


class Event(models.Model, EventMixin):
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    name = models.CharField(max_length=150)
    date = models.DateTimeField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType)

    class Meta:
        db_table = 'simple_events_event'
