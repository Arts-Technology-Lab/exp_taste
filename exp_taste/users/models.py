from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models.fields import PositiveSmallIntegerField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import pytz

class User(AbstractUser):
    """Default user for Expensive Taste."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    timezone = CharField(
        "Preferred Time Zone",
        max_length=30,
        choices=((tz, tz) for tz in pytz.common_timezones),
        default="UTC"
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
