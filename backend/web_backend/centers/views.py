from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status

from users.views import *
from medical_centers.serializers import *
from .serializers import *
from medical_centers.models import *

from django.shortcuts import redirect
from django.urls import reverse


class MedicalCentersView(APIView):
    def get(self, request, id=None):
        # no need to login

        if id is not None:
            try: 
                medcent = MedicalCenter.objects.get(id=id)
            except:
                return Response(
                    {"message": "Medical center is not found!"},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = MedicalCenterSerializer(medcent)

            response = Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
            return response
        
        # else
        try: 
            medcents = MedicalCenter.objects.all()
        except:
            return Response(
                {"message": "Not found any medical center record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = MedicalCenterListSerializer(medcents, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response