from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import UserRegistrationSerializer, UserRetrieveSerializer, UpdatePasswordSerializer


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserRegistrationSerializer


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # def delete(self, request, *args, **kwargs):
    #     logout(request)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
