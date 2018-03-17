from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    about = models.TextField(null=True)

    def __str__(self):
        return self.username

    @property
    def twits_count(self):
        return self.twits.all().count()

    @property
    def votes_count(self):
        return self.votes.all().count()

