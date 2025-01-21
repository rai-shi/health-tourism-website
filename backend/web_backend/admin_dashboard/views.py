from django.conf import settings

from django.contrib.admin import site
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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
from users.serializers import UserSerializers

from medical_centers.models import MedicalCenter, Speciality, Procedure, HealthInstitutions
from medical_centers.serializers import HealthInstitutionsSerializer

from specialities.serializers import SpecialitySerializer, ProcedureSerializer

from patient.models import Patient, MedicalCenterRequest
from .serializers import RequestsSerializer

from destinations.models import Destination
from destinations.serializers import DestinationSerializer, DestinationListSerializer


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
            response = Response() 
            response.set_cookie(key="jwt", value=token, httponly=True) 
            return response 

        return render(request, 'admin/login.html', {'form': form})

# ! base adminde logout yaptığım halde burada logout olmuyor
class AdminLogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        response = Response() 
        response.delete_cookie("jwt")
        logout(request) 
        response.data= {
            "message": "successfully logout"
        }
        return response

class AdminUserCreateView(APIView):
    def post(self, request):
        pass

class AdminUsersView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try:
            users = User.objects.all()
        except:
            return Response(
                    {"message": "Not found any user!"},
                    status = status.HTTP_404_NOT_FOUND
                )
        serializer = UserSerializers(users, many=True)
        users_dict = serializer.data
        # ! user verileri anonimleştirilebilir
        for user in users_dict:
            try:
                user_instance = User.objects.get(id=user['id'])  
            except:
                return Response(
                    {"message": "User is not found!"},
                    status = status.HTTP_404_NOT_FOUND
                )
            if hasattr(user_instance, 'medical_center'): 
                user['role'] = 'medical-center'
            elif hasattr(user_instance, 'patient'): 
                user['role'] = 'patient'
            else:
                user['role'] = 'admin' 

        return Response(
                            users_dict,
                            status=status.HTTP_201_CREATED
                        )
    
class AdminSpecialitiesView(APIView):
    def get(self, request, id=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try: 
            specialities = Speciality.objects.all()
        except:
            return Response(
                {"message": "Not found any speciality record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = SpecialitySerializer(specialities, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response

    def post(self, request, id=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        # procedure creation
        if id is not None:
            serializer = ProcedureSerializer(data=request.data)
            if serializer.is_valid():
                    serializer.save()
            else:
                return Response(serializer.errors, status=400)

            response = Response(
                {
                    "message": "Procedure is successfully added.",
                },
                status=status.HTTP_200_OK
            )
            return response
        # speciality creation
        # name = request.data.get("name")
        # code = request.data.get("code")
        serializer = SpecialitySerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "Speciality is successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def delete(self, request, id):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        if id is not None:
            try:
                instance = Speciality.objects.get(id=id)
            except Speciality.DoesNotExist:
                return Response(
                    {"message": "Speciality is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            name = instance.name
            instance.delete()
            return Response(
                {"message": f"{name} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        speciality_ids = request.data.get("ids", [])
        if not speciality_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = Speciality.objects.filter(id__in=speciality_ids).delete()
        return Response(
            {"message": f"{deleted_count} speciality successfully deleted."},
            status=status.HTTP_200_OK
        )

class AdminProceduresView(APIView):
    # def get(self, request):
    #     pass
    def delete(self, request, speciality_id, procedure_id ):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try:
            instance = Procedure.objects.get(id=procedure_id)
        except Procedure.DoesNotExist:
            return Response(
                {"message": "Procedure is not found!"},
                status=status.HTTP_404_NOT_FOUND
            )

        name = instance.name
        instance.delete()
        return Response(
            {"message": f"{name} is successfully deleted."},
            status=status.HTTP_200_OK
        )


class AdminInsurancesView(APIView):
    def get(self, request, id=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try: 
            insurances = HealthInstitutions.objects.all()
        except:
            return Response(
                {"message": "Not found any insurance record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = HealthInstitutionsSerializer(insurances, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response

    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        serializer = HealthInstitutionsSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "Health Insurance is successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def delete(self, request, id):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        if id is not None:
            try:
                instance = HealthInstitutions.objects.get(id=id)
            except HealthInstitutions.DoesNotExist:
                return Response(
                    {"message": "Speciality is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            name = instance.name
            instance.delete()
            return Response(
                {"message": f"{name} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        insurance_ids = request.data.get("ids", [])
        if not insurance_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = HealthInstitutions.objects.filter(id__in=insurance_ids).delete()
        return Response(
            {"message": f"{deleted_count} insurance successfully deleted."},
            status=status.HTTP_200_OK
        )


class AdminDestinationsView(APIView):
    def get(self, request, id=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        if id is not None:
            try: 
                destination = Destination.objects.get(id=id)
            except:
                return Response(
                    {"message": "Destination is not found!"},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = DestinationSerializer(destination)

            response = Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
            return response
        
        # else
        try: 
            destinations = Destination.objects.all()
        except:
            return Response(
                {"message": "Not found any destination record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = DestinationListSerializer(destinations, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response

    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "Destination is successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def put(self, request, id):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try:
            dest_instance = Destination.objects.get(id=id)
        except:
             return Response(
                    {"message": "Destination is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )
        serializer = DestinationSerializer(dest_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "message": "Destination information is successfully updated.",
                },
                status=status.HTTP_200_OK
            )   
            return response
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        if id is not None:
            try:
                instance = Destination.objects.get(id=id)
            except Destination.DoesNotExist:
                return Response(
                    {"message": "Destination is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            name = instance.name
            instance.delete()
            return Response(
                {"message": f"Destination {name} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        destination_ids = request.data.get("ids", [])
        if not destination_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = Destination.objects.filter(id__in=destination_ids).delete()
        return Response(
            {"message": f"{deleted_count} destination successfully deleted."},
            status=status.HTTP_200_OK
        )


class AdminRequestsView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user = getUserByID(payload)
        if not user.is_superuser:
            return Response(
                            {"message": "You must be a superuser to access this page."},
                            status=status.HTTP_403_FORBIDDEN
                        )
        try:
            requests = MedicalCenterRequest.objects.all()
        except:
            return Response (
                {
                    "message" : "Requests are not found!" 
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
        serializer = RequestsSerializer(requests, many = True)

        return Response(
                    {
                        "requests" : serializer.data,
                    },
                    status=status.HTTP_200_OK
                )  

class AdminBlogView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        pass