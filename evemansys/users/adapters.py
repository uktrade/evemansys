from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class CustomSocialAccountAdapter(SocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user_model = get_user_model()
        if sociallogin.user is None and sociallogin.emails:
            if len(sociallogin.emails) > 1:
                raise ValueError('Social Login has more than one email address.')

            email = sociallogin.emails[0]
            # sociallogin.connect(request, user)

        # except user_model.DoesNotExist:
        #     pass


class CustomAccountAdapter(AccountAdapter):
    pass
