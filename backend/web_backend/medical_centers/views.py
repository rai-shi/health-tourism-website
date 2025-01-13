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


class UpdateMedicalCenterInfoView(APIView):
    def put(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)

        serializer = UpdateMedicalCenterSerializer(instance=med_cent, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Medical center updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # # get the medical center data 
        # center_name     = request.data.get("center-name")
        # center_type     = request.data.get("center-type")
        # city            = request.data.get("city")
        # contact_number  = request.data.get("contact-number")
        # mail_address    = request.data.get("mail-address")
        # web_site        = request.data.get("web-site")
        # preview_text    = request.data.get("preview-text")
        # overview_text   = request.data.get("overview-text")
        
        # # id'ler ile gelsin
        # # ! ön tarafa da id'ler, kod ve isim gönderilir. 
        # specialities    = request.data.get("specialities", [])
        # procedures      = request.data.get("procedures", [])
        # contracted_health_institutions = request.data.get("health-institutions", [])


