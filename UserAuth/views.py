from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import CustomUserSerializer, UserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class AddUser(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        permissions_classes = (IsAuthenticated,)
        user = request.user.customuser
        serializer = self.serializer_class(user)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # print(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {
                    "error": ["username is already taken"]
                },
                status=status.HTTP_400_BAD_REQUEST)


class ChangePermission(APIView):
    # currently for debugging purposes
    # permission_classes = (AllowAny, )

    def post(self, request, format=None):
        print(request.data)
        try:
            user = get_object_or_404(CustomUser, id=request.data.get('id'))
            if request.data.get('manager'):
                user.is_manager = request.data.get('manager')
            if request.data.get('admin'):
                user.is_admin = request.data.get('admin')

            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CheckUser(APIView):
    serializer_class = UserSerializer
    # permission_classes = (AllowAny, )
    def get(self, request, format=None):
        permissions_classes = (IsAuthenticated,)
        user = request.user.customuser
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



