from django.conf import settings

from django.contrib.admin import site
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseForbidden

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
from users.views import generateToken, isTokenValid, getUserByID


class AdminView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        
        return Response(
                            {"message": "admin landing page"},
                            status=status.HTTP_201_CREATED
                        )
    
class AdminLoginView(APIView):
    def get(self, request):
        # Giriş formu
        form = AuthenticationForm()
        return render(request, 'admin/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.is_superuser:
                messages.error(request, "You must be a superuser to access this page.")
                return redirect('/admin-dashboard/login') 

            login(request, user)
            token = generateToken(user=user)  
            response = HttpResponseRedirect('/admin-dashboard/')  
            response.set_cookie(key="jwt", value=token, httponly=True)  
            return response 

        return render(request, 'admin/login.html', {'form': form})

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