from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from evemansys.users.models import User

QUESTION_TYPES = [('yes_no', 'Yes-No'), ('multichoice', 'Multi-choice'), ('onechoice', 'One-choice'), ('freetext', 'Free Text')]
TICKET_CHOICES = [('payed', 'Payed'), ('free', 'Free'), ('eoi', 'Expresion of Interest')]


class BaseModel(models.Model):
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(db_index=True, auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    address = models.TextField(null=True, blank=True)
    postcode = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.address


class Question(models.Model):
    question = models.TextField(blank=True, null=False)
    answer_type = models.CharField(choices=QUESTION_TYPES, max_length=20)
    context = JSONField(default={})

    def __str__(self):
        return self.question


class Sponsor(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    start_date_time = models.DateTimeField(db_index=True, null=True, blank=True)
    end_date_time = models.DateTimeField(db_index=True, null=True, blank=True)

    #TODO multiday multilocation in the future
    location = models.ForeignKey(Address, blank=True, null=True)
    questions = models.ManyToManyField(Question, through='EventQuestion')
    sponsors = models.ManyToManyField(Sponsor, through='EventSponsor')

    live = models.BooleanField(default=False, db_index=True)
    template = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.title


class EventSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return '{} {} [{}]'.format(self.order, self.sponsor, self.event)


class EventQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(db_index=True)

    def __str__(self):
        return '{} {}'.format(self.question, self.event)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answer', db_index=True)
    user = models.ForeignKey(User, related_name='answer', db_index=True)
    event = models.ForeignKey(Event, related_name='answer', db_index=True)
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=20)
    context = JSONField(default={})

    def __str__(self):
        return self.question_type


class Ticket(models.Model):
    event = models.ForeignKey(Event, related_name='ticket', on_delete=models.CASCADE)
    max_tickets = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=150)
    type = models.CharField(choices=TICKET_CHOICES, max_length=20)

    def __str__(self):
        return self.name


class UserTicket(BaseModel):
    uuid = models.UUIDField(db_index=True)
    ticket = models.ForeignKey(Ticket, db_index=True, related_name='user_ticket')
    user = models.ForeignKey(User, db_index=True, related_name='user_ticket')

    def __str__(self):
        return '{} {}'.format(self.user, self.uuid)
