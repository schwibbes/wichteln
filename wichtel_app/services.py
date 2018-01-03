from .models import Event, Participant
import random
import logging

logger = logging.getLogger(__name__)

def to_n(participants):
    return [x.name for x in participants]


def without_elem(elem, participants):
    result = {x for x in participants if x != elem}
    logger.debug("[without_elem: %s] in: %s, out: %s", elem.name, to_n(participants), to_n(result))
    return result


def no_incoming(participants):
    result = {x for x in participants if x not in {y.assignedTo for y in participants}}
    logger.debug("[no_incoming] in: %s, out: %s", to_n(participants), to_n(result))
    return result


def no_outgoing(participants):
    result = {x for x in participants if not x.assignedTo}
    logger.debug("[no_outgoing] in: %s, out: %s", to_n(participants), to_n(result))
    return result


def distribute(participants):
    give = random.choice(participants)
    while not _is_complete(participants):
        free = without_elem(give, participants) & no_incoming(participants)
        logger.debug("free %s ", to_n(free))
        get = random.choice(list(free))
        give.assignedTo = get
        logger.debug("%s gives to %s", give.name, get.name)
        give = get
        logger.debug(participants)
    return participants


def finish(id):
    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    if not is_clean(id):
        raise ValueError("event inconsistent")
    for p in distribute(_participants):
        p.save()
    if not is_complete(id):
        raise ValueError("event not complete")


def can_complete(id):
    _participants = Participant.objects.filter(event__id=id)
    return len(_participants) >= 2 and not _is_complete(_participants)


def is_clean(id):
    _participants = Participant.objects.filter(event__id=id)
    return len(no_outgoing(_participants)) == len(no_incoming(_participants)) == len(_participants)


def can_add_participant(id):
    return is_clean(id)


def _is_complete(participants):
    return len(no_outgoing(participants)) == 0 and len(no_incoming(participants)) == 0


def is_complete(id):
    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    return len(_participants) > 0 and _is_complete(_participants)

def clear_all(id):
    _event = Event.objects.get(pk=id)
    _participants = Participant.objects.filter(event__id=id)
    for p in _participants:
        p.assignedTo = None
        p.save()
        logger.info("cleared %s", p)
