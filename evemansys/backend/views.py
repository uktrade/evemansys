import functools
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, render_to_response
from formtools.wizard.views import SessionWizardView

from evemansys.backend.forms import CreateEventForm1, CreateEventForm2, CreateEventForm3
from evemansys.events.entities import Events


def is_employee(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        if request and hasattr(request, 'user') and hasattr(request.user, 'is_employee') and request.user.is_employee:
            return f(request, *args, **kwargs)
        return HttpResponseForbidden()
    return wrapper


@is_employee
def dashboard(request):
    data = dict()
    data['user'] = request.user
    data['live_events'] = Events.get_live_events(user=request.user)
    data['drafts'] = Events.get_draft_events(user=request.user)
    data['templates'] = Events.get_template_events(user=request.user)
    data['past_events'] = Events.get_past_events(user=request.user)

    return render(
        request=request,
        template_name='backend/dashboard.html',
        context=data)


class CreateEventWizard(SessionWizardView):
    form_list = [CreateEventForm1, CreateEventForm2, CreateEventForm3]
    template_name = 'backend/wizard_form.html'

    def done(self, form_list, **kwargs):
        return render_to_response('backend/event_wizard_form_done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

