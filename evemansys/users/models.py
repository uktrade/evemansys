from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)


class Employee(models.Model):
    base_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} [{}]'.format(self.username, 'Employee')

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class ExternalUser(models.Model):
    base_user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.username
