from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "github_repository_browser.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import github_repository_browser.users.signals  # noqa F401
        except ImportError:
            pass
