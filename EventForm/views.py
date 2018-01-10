from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from UserAuth.models import CustomUser
from .serializers import NewEventsSerializer, EventRegistrationSerializer
from .models import NewEvents, EventRegistration

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

import traceback
# from rest_framework.serializers import Serializer


class NewEventsView(APIView):
    serializer_class = NewEventsSerializer
    # permission_classes = (AllowAny, )

    def get(self, request, format=None):
        user = request.user.customuser
        events = NewEvents.objects.filter(user=user)
        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if (int(request.user.customuser.id) != int(request.data.get('user_id')) or request.user.customuser.is_manager != True) and request.user.customuser.is_admin is False:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(status=500)


class EventRegistrationView(APIView):
    serializer_class = EventRegistrationSerializer

    def get(self, request, format=None):
        user = request.user.customuser
        registrations = EventRegistration.objects.filter(applied_by=user)
        serializer = self.serializer_class(registrations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if int(request.user.customuser.id) != int(request.data.get('applied_by')) and request.user.customuser.is_admin is False:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            print(traceback.format_exc())
            return Response(status=500)

    def delete(self, request, format=None):
        try:
            event_reg_id = request.data.get('id')
            if event_reg_id is None:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            event_reg = EventRegistration.objects.get(id=event_reg_id)
            if int(event_reg.applied_by.user.id) == int(request.user.customuser.id) or int(event_reg.event.user.id) == int(request.user.customuser.id):
                event_reg.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception:
            print(traceback.format_exc())
            return Response(status=500)
