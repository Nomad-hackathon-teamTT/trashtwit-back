from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from . import models as twits_models
from trashtwit_back.users import models as user_models


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'id',
            'username',
        )

class CommentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)  # Read only to prevent user from changing the creator of the comment.

    class Meta:
        model = twits_models.Comment
        fields = '__all__'

class TwitSerializer(TaggitSerializer, DynamicFieldsModelSerializer):
    creator = UserSerializer()
    comment = CommentSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = twits_models.Twit
        fields = (
            'id',
            'creator',
            'twit',
            'comment',
            'vote_count',
            'comment_count',
            'tags'
        )