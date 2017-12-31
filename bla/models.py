from django.db import models
import uuid


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    creator_uuid = models.CharField(max_length=36, default=uuid.uuid4)

    def __str__(self):
        return "%s@%s" % (self.name, self.date)


class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    code = models.CharField(max_length=4, default='1234')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assignedTo = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s<%s> (to: %s)" % (self.name, self.email, self.assignedTo.name if self.assignedTo else '')
