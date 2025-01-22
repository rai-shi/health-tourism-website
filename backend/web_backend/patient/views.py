from django.shortcuts import render
from users.views import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializers
from .serializers import PatientSerializers, MedicalCenterRequestSerializer, MedicalCenterRequestViewSerializer
from .models import Patient, MedicalCenterRequest
from cities_light.models import City, Country

def getPatientByID(payload):
    user = getUserByID(payload=payload)
    patient = Patient.objects.filter(user=user.id).first()
    if not patient:
        raise AuthenticationFailed("Patient is not found!")
    
    return (user, patient)
    
def getCityName(id):
    city = City.objects.filter(id=id).first()
    return city.name

def getCountryName(id):
    country = Country.objects.filter(id=id).first()
    return country.name

# GET
class PatientView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        
        user, patient = getPatientByID(payload=payload)

        # make the data json valid
        user_serializer = UserSerializers(user)
        patient_serializer = PatientSerializers(patient)

        response = {
            "user": user_serializer.data,
            "patient":patient_serializer.data   
        }
        return Response(response)
    
# POST
class UpdatePersonalInfoView(APIView):
    def post(self, request):

        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)

        # get the personal data
        gender          = request.data.get("gender")
        birthday        = request.data.get("birthday")
        phone_number    = request.data.get("phone_number")
        country         = request.data.get("country")
        city            = request.data.get("city")

        city_object = City.objects.filter(name=city).first()
        # country kodu geldiğini varsayıyorum, Turkey : TR
        country_object = Country.objects.filter(code2=country).first()

        patient.gender          = gender
        patient.birthday        = birthday
        patient.phone_number    = phone_number
        patient.country         = country_object
        patient.city            = city_object

        patient.save()

        response = Response(
            {
                "message": "Personal information is successfully updated.",
            },
            status=status.HTTP_200_OK
        )
        return response


# POST
class RequestsView(APIView):
    def post(self, request):
        print("patient medical center request")
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)
        data = request.data

        data['patient'] = patient.id 

        city_object = City.objects.filter(name=data["city"]).first()
        country_object = Country.objects.filter(code2=data["country"]).first() 
        data["city"] = city_object.id
        data["country"] = country_object.id

        serializer = MedicalCenterRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "message": "Medical Center request is successfully updated.",
                    "request" : serializer.data,
                },
                status=status.HTTP_200_OK
            )   
            return response
        return Response(serializer.errors, status=400)

    def get(self, request):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)
        # get patient requests
        try:
            instance = MedicalCenterRequest.objects.filter( patient = patient.id )
        except:
            return Response (
                {
                    "message" : "Requests are not found!" 
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
        serializer = MedicalCenterRequestViewSerializer(instance, many = True)

        requests = []
        for request in serializer.data:
            print(request)
            data = {
                "id" : request["id"],
                "medical_center": request["medical_center"],
                "created_at": request["created_at"],
                "speciality":request["speciality"]["name"],
                "procedure":request["procedure"]["name"]
            }
            requests.append(data)
        

        return Response(
                    {
                        "requests" : requests,
                    },
                    status=status.HTTP_200_OK
                )   

class RequestView(APIView):
    def get(self, request, id):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)
        # get patient specified request
        try:
            request = MedicalCenterRequest.objects.get( id=id )
        except:
            return Response (
                {
                    "message" : "Request is not found!" 
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
        serializer = MedicalCenterRequestViewSerializer(request)

        return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )   


class RequestToMedicalCenterView(APIView):
    def post(self, request, medcent_id):
        print("medical center request")
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)
        data = request.data

        data['patient'] = patient.id 
        data['medical_center'] = medcent_id

        city_object = City.objects.filter(name=data["city"]).first()
        country_object = Country.objects.filter(code2=data["country"]).first() 
        data["city"] = city_object.id
        data["country"] = country_object.id
        
        print(data)

        serializer = MedicalCenterRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "message": "Medical Center request is successfully updated.",
                    "request" : serializer.data,
                },
                status=status.HTTP_200_OK
            )   
            return response
        return Response(serializer.errors, status=400)