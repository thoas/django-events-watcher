from datetime import datetime

from django import test
from django.contrib.contenttypes.models import ContentType

from .models import Poll

from simple_events.models import Event

class EventTest(test.TestCase):
    def test_create_basic_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        self.assertEqual(poll.question, 'WHAT?')

        event = Event.objects.add('first_support', poll)

        self.assertEqual(event.content_object, poll)
        self.assertEqual(event.object_id, poll.pk)

        self.assertEqual(event.content_type, ContentType.objects.get_for_model(poll))

        # check if the date is not None even if we don't set it in add()
        self.assertEqual(event.date is None, False)

        current_date = datetime.now()
        event = Event.objects.add('last_support', poll, date=current_date)

        self.assertEqual(event.date, current_date)

    def test_list_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        event = Event.objects.add('first_support', poll)

        self.assertEqual(Event.objects.retrieve('first_support', poll), event)

        events = Event.objects.list(poll)

        self.assertEqual(list(events), [event])

        events = Event.objects.list('first_support')

        self.assertEqual(list(events), [event])

        polls = []
        events = []

        questions = (
            ('ALLO?', 'last_support'),
            ('HERE?', 'first_fan'),
            ('WHERE?', 'last_fan'),
            ('DONDE?', 'last_fan'),
            ('AQUI?', 'last_fan'),
        )

        for question, name in questions:
            poll = Poll.objects.create(question=question, pub_date=datetime.now())
            polls.append(poll)
            events.append(Event.objects.add(name, poll))

        self.assertEqual(list(Event.objects.list('last_fan')), [events[2], events[3], events[4]])

        self.assertEqual(list(Event.objects.list(polls[2])), [events[2]])

        self.assertEqual(list(Event.objects.list(Poll)), [event] + events)

        self.assertEqual(list(Event.objects.list(5457445)), [])

    def test_remove_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())
        self.assertEqual(poll.question, 'WHAT?')

        event = Event.objects.add('first_support', poll)

        Event.objects.remove('first_support')

        list_obj = Event.objects.list('first_support')

        self.assertEqual(list(list_obj), [])

        poll4 = Poll.objects.create(question='WHERE?', pub_date=datetime.now())
        poll5 = Poll.objects.create(question='DONDE?', pub_date=datetime.now())
        event4 = Event.objects.add('last_fan', poll4)
        event5 = Event.objects.add('last_fan', poll5)

        list_obj = Event.objects.list('last_fan')

        self.assertEqual(list(list_obj), [event4, event5])

        Event.objects.remove('last_fan')

        list_obj_2 = Event.objects.list('last_fan')
        self.assertEqual(list(list_obj_2), [])
