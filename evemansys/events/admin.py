from django.contrib import admin
from evemansys.events.models import Address, Event, Sponsor, EventSponsor, EventQuestion, Question, Ticket, Answer


for model in (Address, Event, Sponsor, EventSponsor, EventQuestion, Question, Ticket, Answer):
    admin.site.register(model)
