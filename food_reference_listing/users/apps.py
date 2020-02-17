from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "food_reference_listing.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import food_reference_listing.users.signals  # noqa F401
        except ImportError:
            pass
