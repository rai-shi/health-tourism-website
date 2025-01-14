from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status

from users.views import *
from .models import *
from .serializers import *

from django.shortcuts import redirect
from django.urls import reverse


# from django.contrib.auth.decorators import login_required
# @login_required

def getMedicalCenterByID(payload):
    user = getUserByID(payload=payload)
    med_cent = MedicalCenter.objects.filter(user=user.id).first()
    if not med_cent:
        # return redirect(reverse("register"))
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
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)

        doctors = request.data.get("doctors")
        for doctor in doctors:
            # Set the related_center field using the retrieved medical center object
            doctor['related_center'] = med_cent.id

            doctor_serializer = DoctorSerializer(data=doctor)
            if doctor_serializer.is_valid():
                doctor_serializer.save()
            else:
                return Response(doctor_serializer.errors, status=400)

        response = Response(
            {
                "message": "Doctors are successfully created.",
            },
            status=status.HTTP_200_OK
        )
        return response
            
    def put():
        pass 

    def get(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        isTokenValid(token=token)

        # if spesific doctor is requested
        if pk is not None:
            try:
                instance = Doctor.objects.get(id=pk)
            except Doctor.DoesNotExist:
                return Response(
                    {"message": "Doctor not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = DoctorSerializer(instance)
            return Response( serializer.data, status=status.HTTP_200_OK )
        
        # if doctors list requested
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK )


    def delete(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        isTokenValid(token=token)

        if pk is not None:
            try:
                instance = Doctor.objects.get(id=pk)
            except Doctor.DoesNotExist:
                return Response(
                    {"message": "Doctor not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            name_surname = f"{instance.title} {instance.name} {instance.surname}"
            instance.delete()
            return Response(
                {"message": f"{name_surname} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        doctor_ids = request.data.get("ids", [])
        if not doctor_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = Doctor.objects.filter(id__in=doctor_ids).delete()
        return Response(
            {"message": f"{deleted_count} doctors successfully deleted."},
            status=status.HTTP_200_OK
        )
