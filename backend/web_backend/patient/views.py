from django.shortcuts import render
from users.views import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializers
from .serializers import PatientSerializers
from .models import Patient

def getPatientByID(payload):
    user = getUserByID(payload=payload)
    patient = Patient.objects.filter(user=user.id).first()
    if not patient:
        raise AuthenticationFailed("Patient not found!")
    
    user_serializer = UserSerializers(user)
    patient_serializer = PatientSerializers(patient)

    response = {
        "user": user_serializer.data,
        "patient":patient_serializer.data   
    }
    return response
    

# GET
class PatientView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        
        response = getPatientByID(payload=payload)

        return Response(response)


# POST
class UpdatePersonalInfoView(APIView):
    def post(self, request):
        pass



# POST
def RequestToMedicalCenter(self, request):
    pass


