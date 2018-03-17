from django.db import models
from trashtwit_back.users.models import User
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager

# Create your models here.
@python_2_unicode_compatible
class TimeStampedModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # Setting 'abstract = True', makes this class to be an abstract class.
        # TimeStampedModel cannot be used as a normal Django model, since it is an abstract base class.
        # It does not generate a database table or have a manager, and cannot be instantiated or saved directly.
        abstract = True

@python_2_unicode_compatible
class Twit(TimeStampedModel):
    """
        Twit Model
    """
    location = models.CharField(max_length=100)
    twit = models.TextField(null=True)
    creator = models.ForeignKey(User, null=True, related_name='twit', on_delete=models.CASCADE)
    tags = TaggableManager()

    @property
    def vote_count(self):
        return self.vote.all().count()

    @property
    def comment_count(self):
        return self.comment.all().count()

    def __str__(self):
        return "{} - {}".format(self.location, self.caption)

    class Meta:
        ordering = ['-create_time']

@python_2_unicode_compatible
class Comment(TimeStampedModel):
    """
        Comment Model
    """
    comment = models.TextField()
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    twit = models.ForeignKey(Twit, null=True, related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.comment)


@python_2_unicode_compatible
class Vote(TimeStampedModel):
    """
        Like Model
    """
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    twit = models.ForeignKey(Twit, null=True, related_name='vote', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
