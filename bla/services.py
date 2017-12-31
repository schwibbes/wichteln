from .models import Event, Participant
import random

#https://stackoverflow.com/questions/12578908/separation-of-business-logic-and-data-access-in-django

def finish(id):
    if not is_clean(id):
        raise ValueError("event inconsistent")

    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    taken = []
    for p in _participants:
        givesTo = random.choice( [x for x in _participants if (x != p) and (x not in taken)] )
        print("%s givesTo %s" % (p, givesTo) )
        taken.append(givesTo)
        p.assignedTo = givesTo
        p.save()
    if not is_complete(id):
        raise ValueError("event not complete")


def can_complete(id):
    _participants = Participant.objects.filter(event__id=id)
    return len(_participants) >= 2 and not is_complete(id)


def is_clean(id):
    _participants = Participant.objects.filter(event__id=id)
    assignedParticipants = [p for p in _participants if p.assignedTo]
    return len(assignedParticipants) == 0


def can_add_participant(id):
    return is_clean(id)


def is_complete(id):
    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    gives_present = set( [p for p in _participants if p.assignedTo] )
    gets_present = set( [ p.assignedTo for p in _participants] )
    print(_participants)
    print(gives_present)
    print(gets_present)
    return len(_participants) > 0 and len(gives_present) == len(_participants) and len(gets_present) == len(_participants)


def clear_all(id):
    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    for p in _participants:
        p.assignedTo = None
        p.save()
        print("cleared %s" % (p))
