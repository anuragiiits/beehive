from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import EventRegistration, NewEvents

from UserAuth.models import CustomUser


class NewEventsSerializer(ModelSerializer):
    user_id = serializers.CharField(source='user.id')

    class Meta(object):
        model = NewEvents
        fields = [
            'user_id',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'description',
            'name',
            'id',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # print(validated_data)
        user_data = validated_data.pop('user')['id']
        user = get_object_or_404(CustomUser, id=user_data)
        new_event = NewEvents.objects.create(user=user, **validated_data)
        return new_event


class EventRegistrationSerializer(ModelSerializer):
    event_id = serializers.CharField(source='event.id')
    applied_by = serializers.CharField(source='applied_by.id')

    class Meta:
        model = EventRegistration
        fields = ['event_id', 'applied_by', 'fullname', 'number', 'id']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_id = validated_data.pop('applied_by')['id']
        user = get_object_or_404(CustomUser, id=user_id)
        event_id = validated_data.pop('event')['id']
        event = get_object_or_404(NewEvents, id=event_id)
        event_reg = EventRegistration.objects.create(
            applied_by=user, event=event, **validated_data)
        return event_reg
