from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError

import jwt, datetime, json, environ, os

from users.models import User


class AdminView(APIView):
    def get(self, request):
        return Response(
                            {"message": "admin landing page"},
                            status=status.HTTP_201_CREATED
                        )
    
class AdminLoginView(APIView):
    def post(self, request):
        pass

class AdminLogoutView(APIView):
    def post(self, request):
        pass

class AdminUserCreateView(APIView):
    def post(self, request):
        pass

class AdminUsersView(APIView):
    def get(self, request):
        return Response(
                            {"message": "admin users list"},
                            status=status.HTTP_201_CREATED
                        )
    
class AdminSpecialitiesView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AdminProceduresView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AdminInsurancesView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AdminDestinationsView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AdminRequestsView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AdminBlogView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass