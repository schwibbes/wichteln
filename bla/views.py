from django.shortcuts import render, redirect
from .models import Event, Participant
from .forms import *
from .services import *

def event_list(request):
    all_events = Event.objects.all()
    context = {'event_list': all_events}
    return render(request, 'bla/event_list.html', context)


def event_detail(request, id):
    _event = Event.objects.get(pk=id)

    _creator_uuid = request.GET.get('creator_uuid')
    if not _creator_uuid:
        _creator_uuid = request.COOKIES.get('%s-creator_uuid' % (_event.id))

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
            Participant.objects.create(
                name=form.cleaned_data['name'], event=_event, email=form.cleaned_data['email'], code=form.cleaned_data['auth_code'])
            response = redirect('event_detail', id=id)
        else:
            context['form_error'] = form.errors
            response = render(request, 'bla/event_detail.html', context)
    else:
        context['form'] = NewParticipantForm()
        response = render(request, 'bla/event_detail.html', context)
    return response


def event_complete(request, id):
    if request.method == "POST":
        finish(id)
        return redirect('event_detail', id=id)


def event_clear(request, id):
    if request.method == "POST":
        clear_all(id)
        return redirect('event_detail', id=id)


def event_new(request):
    if request.method == "POST":
        form = NewEventForm(request.POST)
        if form.is_valid():
            _event = Event.objects.create(
                name=form.cleaned_data['name'], date=form.cleaned_data['date'])
            response = redirect('/bla/events/%d/?creator_uuid=%s' % (_event.id, _event.creator_uuid))
            response.set_cookie('%s-creator_uuid' % (_event.id), _event.creator_uuid)
        else:
            response = render(request, 'bla/event_new.html', {'form': form})
    else:
        form = NewEventForm()
        response = render(request, 'bla/event_new.html', {'form': form})
    return response


def participant_detail(request, id):
    _participant = Participant.objects.get(id=id)
    context = {'participant': _participant}
    if request.method == "POST":
        form = AuthCodeForm(request.POST)
        context['form'] = form
        context['try_auth'] = True
        if form.is_valid():
            context['is_authenticated'] = form.cleaned_data['auth_code'] == _participant.code
        else:
            context['form_error'] = form.errors
        return render(request, 'bla/participant_detail.html', context)
    else:
        form = AuthCodeForm()
        context['form'] = form
        context['is_authenticated'] = False
        return render(request, 'bla/participant_detail.html', context)

