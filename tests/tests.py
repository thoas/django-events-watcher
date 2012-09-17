from datetime import datetime

from django import test
from django.contrib.contenttypes.models import ContentType

from .models import Poll

from simple_events.bridge import backend as events


class EventTest(test.TestCase):
    def test_create_basic_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        self.assertEqual(poll.question, 'WHAT?')

        event = events.add('first_support', poll)

        self.assertEqual(event.content_object, poll)
        self.assertEqual(event.object_id, poll.pk)

        self.assertEqual(event.content_type, ContentType.objects.get_for_model(poll))

        # check if the date is not None even if we don't set it in add()
        self.assertEqual(event.date is None, False)

        current_date = datetime.now()
        event = events.add('last_support', poll, date=current_date)

        self.assertEqual(event.date, current_date)

    def test_list_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        event = events.add('first_support', poll)

        self.assertEqual(events.retrieve('first_support', poll), event)

        event_list = events.list(poll)

        self.assertEqual(list(event_list), [event])

        event_list = events.list('first_support')

        self.assertEqual(list(event_list), [event])

        polls = []
        event_list = []

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
            event_list.append(events.add(name, poll))

        self.assertEqual(list(events.list('last_fan')), [event_list[2], event_list[3], event_list[4]])

        self.assertEqual(list(events.list(polls[2])), [event_list[2]])

        self.assertEqual(list(events.list(Poll)), [event] + event_list)

        self.assertEqual(list(events.list(5457445)), [])

    def test_remove_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())
        self.assertEqual(poll.question, 'WHAT?')

        events.add('first_support', poll)

        events.remove('first_support')

        list_obj = events.list('first_support')

        self.assertEqual(list(list_obj), [])

        poll4 = Poll.objects.create(question='WHERE?', pub_date=datetime.now())
        poll5 = Poll.objects.create(question='DONDE?', pub_date=datetime.now())
        event4 = events.add('last_fan', poll4)
        event5 = events.add('last_fan', poll5)

        list_obj = events.list('last_fan')

        self.assertEqual(list(list_obj), [event4, event5])

        events.remove('last_fan')

        list_obj_2 = events.list('last_fan')
        self.assertEqual(list(list_obj_2), [])
