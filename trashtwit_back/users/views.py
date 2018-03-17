from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# from django.core.urlresolvers import reverse
# from django.views.generic import DetailView, ListView, RedirectView, UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin

from . import models
from . import serializers


class ProfilePage(APIView):

    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(data="There is no user named {}.".format(username), status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(data="There is no user named {}.".format(username), status=status.HTTP_404_NOT_FOUND)

        if found_user.username == request.user.username:
            serializer = serializers.ProfileSerializer(found_user,
                                                           fields=('username'),
                                                           data=request.data,
                                                           partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
