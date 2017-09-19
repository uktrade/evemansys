from allauth.account.models import EmailAddress
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from evemansys.users.models import Employee, ExternalUser


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class CustomSocialAccountAdapter(SocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if len(sociallogin.email_addresses) > 1:
            raise ValueError('Social Login has more than one email address.')

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)

    def new_user(self, request, sociallogin):
        user = super().new_user(request, sociallogin)
        if sociallogin.account.provider == 'ditsso-internal':
            extended_user = Employee()
        elif sociallogin.account.provider == 'ditsso':
            extended_user = ExternalUser()
        else:
            return user

        extended_user.populate(user=user, request=request, sociallogin=sociallogin)
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        for user_class in ('externaluser', 'employee'):
            if hasattr(user, user_class):
                user_instance = getattr(user, user_class)
                user_instance.save()
        return user


class CustomAccountAdapter(AccountAdapter):
    pass
