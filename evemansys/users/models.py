from django.contrib.auth.models import AbstractUser, Group
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

EMPLOYEE_GROUP_NAME = 'employee'


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    # Maybe we should check the group = 'employee' for consistency
    @property
    def is_employee(self):
        if hasattr(self, 'employee'):
            return True
        return False


class Employee(models.Model):
    base_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} [{}]'.format(self.base_user.username, 'Employee')

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.base_user.username})

    def populate(self, user, request, sociallogin):
        self.base_user = user

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.base_user_id = self.base_user.id
        super().save(force_insert, force_update, using, update_fields)
        employee_group = Group.objects.get(name='employee')
        self.base_user.groups.add(employee_group)


class ExternalUser(models.Model):
    base_user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.base_user.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.base_user.username})

    def populate(self, user, request, sociallogin):
        self.base_user = user

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.base_user_id = self.base_user.id
        super().save(force_insert, force_update, using, update_fields)
