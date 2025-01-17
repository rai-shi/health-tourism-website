from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.views import *
from medical_centers.models import Speciality, Procedure
from .serializers import *

from django.shortcuts import redirect
from django.urls import reverse

class SpecialitiesView(APIView):
    def get(self, request):
        # no need to login

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

        