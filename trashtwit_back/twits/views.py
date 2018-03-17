from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from trashtwit_back.twits import models
from . import serializers
from . import models

class Feed(APIView):
    def post(self, request, format=None):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        nearby_twits = models.Twit.objects.filter(latitude__lt=latitude + 50,
                                                  latitude__gt=latitude - 50,
                                                  longitude__lt=longitude + 50,
                                                  longitude__gt=longitude - 50)
        serializer = serializers.TwitSerializer(nearby_twits, many=True)

        # TO DO: Delete the ones that past 24 hrs

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Twit(APIView):

    def post(self, request, format=None):

        user = request.user
        serializer = serializers.TwitSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(creator=user, latitude=request.data.get('latitude'), longitude=request.data.get('longitude'))

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                                                fields=('twit'),
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


class CommentOnTwit(APIView):

    def post(self, request, twit_id, format=None):

        user = request.user

        try:
            found_twit = models.TWit.objects.get(id=twit_id)
        except models.Twit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_twit)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)