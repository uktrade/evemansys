from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'evemansys.events'
    verbose_name = "Events"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
