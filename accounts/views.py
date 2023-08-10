from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes
from django_email_verification import verify_view, verify_token, send_email
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, 
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    )

from .models import User
from .serializers import (
                            UserSerializer, 
                        )
# Create your views here.


class UserAPIView(CreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response_data = {
            'status': 'success',
            'message': 'Mail is sent to user email address for account verification',
            'data': response.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
        # return redirect('login')

    def perform_create(self, serializer):
        user = serializer.save(has_accepted_terms=True)
        send_email(user)


@verify_view
@api_view(['GET'])
def confirm(request, token):
    success, user = verify_token(token)
    return Response({"detail": f'Account verified, {user.email}' if success else 'Invalid token'}, status=status.HTTP_200_OK)


class EmailAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # A backend authenticated the credentials
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'email': user.email,
                })
            else:
            # No backend authenticated the credentials
                return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)