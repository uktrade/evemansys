from django.utils.timezone import now

from evemansys.events.models import Event


class Events(Event):
    class Meta:
        proxy = True

    @classmethod
    def _get_events_queryset(cls, live=True, template=False):
        return cls.objects.filter(live=live, template=template)

    @classmethod
    def get_live_events(cls, user):
        return cls._get_events_queryset().filter(start_date_time__gte=now())

    @classmethod
    def get_past_events(cls, user):
        return cls._get_events_queryset().filter(start_date_time__lte=now())

    @classmethod
    def get_draft_events(cls, user):
        return cls._get_events_queryset(live=False)

    @classmethod
    def get_template_events(cls, user):
        return cls._get_events_queryset(template=True, live=False)

