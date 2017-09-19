from django.conf.urls import url

from evemansys.backend.views import CreateEventWizard
from . import views

urlpatterns = [
    url(regex=r'^$', view=views.dashboard, name='Dashboard'),
    url(r'^create_event/$', CreateEventWizard.as_view(), name='create-event'),
]
