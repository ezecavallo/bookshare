"""Users views."""

# Models
from bookshare.users.models import User
from bookshare.circles.models import Circle
from rest_framework import status

# Permissions
from bookshare.users.permissions import IsAccountOwner
from rest_framework.permissions import AllowAny, IsAuthenticated

# Serializers
from bookshare.users.serializers import (
    UserModelSerializer,
    CreateUserSerializer,
    CustomJSONWebTokenSerializer,
    VerifyAccountSerializer,
    ProfileModelSerializer,
)
from rest_framework_jwt.serializers import (
    VerifyJSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer
)
from bookshare.circles.serializers import CircleModelSerializer

# REST Framework
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# REST Framwork JWT
from rest_framework_jwt.settings import api_settings
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

# Utils
from datetime import datetime


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    """
    User viewset.
    Handle the login and signup.
    """

    queryset = User.objects.filter(is_client=True, is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_serializer_class(self):

        if self.action == 'login':
            return CustomJSONWebTokenSerializer
        if self.action == 'signup':
            return CreateUserSerializer

    def get_permissions(self):
        """
        Define permissions based on actions.
        """
        if self.action in ['login', 'signup', 'verify', 'api_refresh', 'api_verify']:
            permissions_class = [AllowAny]
        elif self.action in ['partial_update', 'update', 'retrieve', 'profile']:
            permissions_class = [IsAuthenticated, IsAccountOwner]
        else:
            permissions_class = [IsAuthenticated]

        return [permission() for permission in permissions_class]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """User sign up."""

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    # API JWT REST Framework
    @action(detail=False, methods=['POST'])
    def login(self, request):
        """User login."""
        from django.contrib.auth import authenticate, login

        serializer = CustomJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=request.data['email'], password=request.data['password'])
            login(request, user)
            response = Response('sad')
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def login(self, request):
    #     """User login."""
    #
    #     serializer = CustomJSONWebTokenSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.object.get('user') or request.user
    #         token = serializer.object.get('token')
    #         response_data = jwt_response_payload_handler(token, user, request)
    #         response = Response(response_data)
    #         if api_settings.JWT_AUTH_COOKIE:
    #             expiration = (datetime.utcnow() +
    #                           api_settings.JWT_EXPIRATION_DELTA)
    #             response.set_cookie(api_settings.JWT_AUTH_COOKIE,
    #                                 token,
    #                                 expires=expiration,
    #                                 httponly=True)
    #         return response
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        """Verify user account."""

        serializer = VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now go and share some books.'}
        return Response(data, status=status.HTTP_200_OK)

    # Profile
    @action(detail=True, methods=['PUT', 'PATCH'])
    def profile(self, request):
        """Update profile data."""

        user = self.get_object()
        profile = user.profile
        partial = request.methods = 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserModelSerializer(user).data

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""

        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)

        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response
