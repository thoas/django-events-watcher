from datetime import datetime

from django import test
from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings

from .models import Poll, Choice

from simple_events.utils import load_class


class DatabaseEventTest(test.TestCase):
    def setUp(self):
        self.backend = load_class('simple_events.backends.database.DatabaseBackend')()

    def test_create_basic_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        self.assertEqual(poll.question, 'WHAT?')

        event = self.backend.add('first_support', poll)

        self.assertEqual(event.content_object, poll)

        self.assertEqual(event.object_id, poll.pk)

        self.assertEqual(event.content_type, ContentType.objects.get_for_model(poll))

        # check if the date is not None even if we don't set it in add()
        self.assertEqual(event.date is None, False)

        current_date = datetime.now()
        event = self.backend.add('last_support', poll, date=current_date)

        self.assertEqual(event.date, current_date)

    def test_list_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())

        event = self.backend.add('first_support', poll)

        self.assertEqual(self.backend.retrieve('first_support', poll), event)

        event_list = self.backend.list(poll)

        self.assertEqual(list(event_list), [event])

        event_list = self.backend.list('first_support')

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
            event_list.append(self.backend.add(name, poll))

        self.assertEqual(list(self.backend.list('last_fan')), [event_list[2], event_list[3], event_list[4]])

        self.assertEqual(list(self.backend.list(polls[2])), [event_list[2]])

        self.assertEqual(list(self.backend.list(Poll)), [event] + event_list)

        self.assertEqual(list(self.backend.list(5457445)), [])

    def test_remove_event(self):
        poll = Poll.objects.create(question='WHAT?', pub_date=datetime.now())
        self.assertEqual(poll.question, 'WHAT?')

        self.backend.add('first_support', poll)

        self.backend.remove('first_support')

        list_obj = self.backend.list('first_support')

        self.assertEqual(list(list_obj), [])

        poll4 = Poll.objects.create(question='WHERE?', pub_date=datetime.now())
        poll5 = Poll.objects.create(question='DONDE?', pub_date=datetime.now())
        event4 = self.backend.add('last_fan', poll4)
        event5 = self.backend.add('last_fan', poll5)

        list_obj = self.backend.list('last_fan')

        self.assertEqual(list(list_obj), [event4, event5])

        self.backend.remove('last_fan')

        list_obj_2 = self.backend.list('last_fan')
        self.assertEqual(list(list_obj_2), [])

    def test_watch(self):
        poll = Poll.objects.create(question='Y U NO WORK?', pub_date=datetime.now())

        choice = Choice.objects.create(poll=poll, choice='YES', votes=0)

        self.backend.watch(Choice, 'votes_higher_than_zero', lambda initial_data, instance: initial_data['votes'] <= 0 and instance.votes > 0)

        choice.votes = 1
        choice.save()

        events = self.backend.list('votes_higher_than_zero')

        self.assertEqual(len(events), 1)

        event = events[0]

        self.assertEqual(event.name, 'votes_higher_than_zero')
        self.assertEqual(event.content_object, choice)


@override_settings(INSTALLED_APPS=[],
                   SIMPLE_EVENTS_BACKEND='simple_self.backend.backends.redis.RedisBackend')
class RedisEventTest(DatabaseEventTest):
    def setUp(self):
        self.backend = load_class('simple_events.backends.redis.RedisBackend')()
        import redisco
        redisco.connection.flushdb()
