from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status

from users.views import *
from .models import *
from .serializers import *


def getMedicalCenterByID(payload):
    user = getUserByID(payload=payload)
    med_cent = MedicalCenter.objects.filter(user=user.id).first()
    if not med_cent:
        raise AuthenticationFailed("Medical center is not found!")
    
    return (user, med_cent)

class MedicalCenterView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)

        user_serializer = UserSerializers(user)
        med_cent_serializer = MedicalCenterSerializer(med_cent)

        response = {
            "user": user_serializer.data,
            "med-cent":med_cent_serializer.data   
        }
        return Response(response)
    
    def put(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)

        serializer = MedicalCenterUpdateSerializer(med_cent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = Response(
            {
                "message": "Medical Center information is successfully updated.",
            },
            status=status.HTTP_200_OK
            )   
            return response
        return Response(serializer.errors, status=400)


class MedicalCenterDoctorsView(APIView):
    def post():
        pass 
    def put():
        pass 
    def delete():
        pass 