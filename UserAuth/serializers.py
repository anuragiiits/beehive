from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser, User


class CustomUserSerializer(ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User()
        user.username = user_data['username']
        user.email = user_data['email']
        user.first_name = user_data['first_name']
        user.set_password(user_data['password'])
        user.last_name = user_data['last_name']
        user.save()
        user_profile = CustomUser.objects.create(user=user)
        return user_profile

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'is_manager',
            'is_admin',
        ]
    
