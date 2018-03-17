from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from trashtwit_back.twits import models
from . import serializers


class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        nearby_users = user.nearby_users.all()

        twit_list = []
        for nusers in nearby_users:
            twits = nusers.twits.all()
            twit_list += [twit for twit in twits]

        my_twits = user.twits.all()[:5]
        twit_list += [twit for twit in my_twits]

        sorted_twit_list = sorted(twit_list, key=lambda tw: tw.create_time, reverse=True)
        serializer = serializers.TwitSerializer(sorted_twit_list, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TwitDetail(APIView):
    def get(self, request, twit_id, format=None):
        user = request.user

        try:
            found_twit = models.Twit.objects.get(id=twit_id)
        except models.Twit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TwitSerializer(found_twit)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, twit_id, format=None):
        user = request.user
        try:
            found_twit = models.Twit.objects.get(id=twit_id, creator=user)
        except models.Twit.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.TwitSerializer(found_twit,
                                                 fields=('image_file',
                                                         'location',
                                                         'caption',),
                                                 data=request.data,
                                                 partial=True)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, twit_id, format=None):
        user = request.user
        try:
            found_twit = models.Twit.objects.get(id=twit_id, creator=user)
        except models.Twit.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        found_twit.delete()
        return Response(status=status.HTTP_200_OK)
