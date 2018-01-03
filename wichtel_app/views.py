from django.shortcuts import render, redirect, reverse
from .models import Event, Participant
from .forms import *
from .services import *
import logging

logger = logging.getLogger(__name__)

def event_list(request):
    all_events = Event.objects.all()
    context = {'event_list': all_events}
    return render(request, 'wichtel_app/event_list.html', context)


def extract_creator_uuid(request, event_id):
    result = request.GET.get('creator_uuid')
    if not result:
        result = request.COOKIES.get('%s-creator_uuid' % (event_id))
    logger.debug("%s", result)
    return result

def event_detail(request, id):
    _event = Event.objects.get(pk=id)
    _creator_uuid =  extract_creator_uuid(request, id)

    context = {'event': _event,
                'participants': Participant.objects.filter(event__id=id),
                'is_complete': is_complete(id),
                'can_complete': can_complete(id),
                'can_add_participant': can_add_participant(id),
                'is_admin': _creator_uuid == str(_event.creator_uuid) }

    if request.method == "POST":
        form = NewParticipantForm(request.POST)
        context['form'] = form
        if form.is_valid():
            _p = Participant.objects.create(
                name=form.cleaned_data['name'], event=_event, email=form.cleaned_data['email'], code=form.cleaned_data['auth_code'])
            response = redirect('event_detail', id=id)
            logger.info("participant created: %s", _p)
        else:
            context['form_error'] = form.errors
            response = render(request, 'wichtel_app/event_detail.html', context)
            logger.warning(form.errors)
    else:
        context['form'] = NewParticipantForm()
        response = render(request, 'wichtel_app/event_detail.html', context)
    return response


def event_complete(request, id):
    if request.method == "POST":
        logger.info("completing event: %s", id)
        finish(id)
        return redirect('event_detail', id=id)


def event_clear(request, id):
    if request.method == "POST":
        logger.warning("clearing event: %s", id)
        clear_all(id)
        return redirect('event_detail', id=id)


def event_new(request):
    if request.method == "POST":
        form = NewEventForm(request.POST)
        if form.is_valid():
            _event = Event.objects.create(
                name=form.cleaned_data['name'], admin=form.cleaned_data['admin_name'], date=form.cleaned_data['date'], description=form.cleaned_data['description'] )
            url = "%s?%s=%s" % (reverse('event_detail', kwargs={'id': _event.id}), 'creator_uuid', _event.creator_uuid)
            response = redirect(url)
            response.set_cookie('%s-creator_uuid' % (_event.id), _event.creator_uuid)
        else:
            response = render(request, 'wichtel_app/event_new.html', {'form': form})
    else:
        form = NewEventForm()
        response = render(request, 'wichtel_app/event_new.html', {'form': form})
    return response


def participant_detail(request, id):
    _participant = Participant.objects.get(id=id)
    context = {'participant': _participant, 'is_complete': is_complete(_participant.event.id)}
    if request.method == "POST":
        form = AuthCodeForm(request.POST)
        context['form'] = form
        context['try_auth'] = True
        if form.is_valid():
            context['is_authenticated'] = form.cleaned_data['auth_code'] == _participant.code
            context['try_auth'] = True
        else:
            context['form_error'] = form.errors
    else:
        form = AuthCodeForm()
        context['form'] = form
        context['is_authenticated'] = False
        context['try_auth'] = False

    return render(request, 'wichtel_app/participant_detail.html', context)

