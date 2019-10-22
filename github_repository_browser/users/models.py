from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def github_token(self) -> str:
        """Fetches Github token in the assumption that there's only one social app"""
        account = self.socialaccount_set.filter(provider="github").first()
        if not account:
            raise AssertionError("User has no associated Github account. Did not login with Github?")
        token_obj = account.socialtoken_set.first()
        if not token_obj:
            raise AssertionError("User has no Github token. Did not login with Github?")
        return token_obj.token
