from django.test import TestCase
from wichtel_app.models import Participant, Event
from wichtel_app.services import distribute

class DistributionTestCase(TestCase):
    def setUp(self):
        e = Event.objects.create(name="anything")
        Participant.objects.create(event=e, name="1")
        Participant.objects.create(event=e, name="2")
        Participant.objects.create(event=e, name="3")
        Participant.objects.create(event=e, name="4")

    def test_distribution_works(self):
        ps = Participant.objects.all()
        for x in distribute(ps):
            self.assertTrue(x.assignedTo, 'Participant has no one to give')
            self.assertTrue(x in [y.assignedTo for y in ps], 'Participant gets from no one')
            self.assertNotEqual(x.assignedTo, x, 'self assignment')
