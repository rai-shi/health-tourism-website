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
    # list all infos
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
    
    # used only one right after registeration for fully updating the whole profile
    def put(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)

        serializer = MedicalCenterUpdateSerializer(med_cent, data=request.data)
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

    # will used when updating the profile partially
    def patch(self, request):
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
    # record of one doctor or many doctor
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        user, med_cent = getMedicalCenterByID(payload=payload)
        doctors = request.data.get("doctors", [])
        # {"doctors": [{}, {}]}
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
            
    def patch(self, request, pk):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        # user, med_cent = getMedicalCenterByID(payload=payload)
        if pk is not None:
            try:
                doctor = Doctor.objects.get(id=pk) 
            except Doctor.DoesNotExist:
                return Response(
                    {"message": "Doctor not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

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
        doctors = Doctor.objects.filter( related_center = medcent.id )
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


def DeleteSpeciality(medcent, specilality_pk):
    try: 
        speciality = medcent.specialities.filter(id= specilality_pk).first()
        # name = speciality.name

        procedures = medcent.procedures.filter(speciality=specilality_pk)
        for procedure in procedures:
            procedure.delete()
        speciality.delete()

    except:
        return Response(
                    {"message": "not found"},
                    status=status.HTTP_404_NOT_FOUND
        )
    
class MedicalCenterSpecialitiesView(APIView):
    def get(self, request, speciality_pk=None):

        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        # if spesific speciality is requested
        if speciality_pk is not None:
            try:
                speciality = medcent.specialities.filter(id= speciality_pk).first()
            except:
                return Response(
                    {"message": "Speciality is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = MedicalCenterSpecialitySerializer(speciality, context= {"medcent":medcent})
            return Response( serializer.data, status=status.HTTP_200_OK )

        # if speciality list requested
        specialities = medcent.specialities.all()

        serializer = MedicalCenterSpecialitySerializer(specialities, many=True, context= {"medcent":medcent})
        return Response( serializer.data, status=status.HTTP_200_OK )
        # return Response( serializer.error, status=status.HTTP_404_NOT_FOUND )
    
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        serializer = MedicalCenterSpecialityUpdateSerializer(medcent, data = request.data)
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "Specialitites and procedures are successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def delete(self, request, speciality_pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)
        
        if speciality_pk is not None:
            DeleteSpeciality(medcent=medcent, specilality_pk=speciality_pk)
            return Response(
                {"message": f"Speciality and its procedures are successfully deleted."},
                status=status.HTTP_200_OK
            )
        speciality_ids = request.data.get("ids", [])
        if not speciality_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for id in speciality_ids:
            DeleteSpeciality(medcent=medcent, specilality_pk=id)
        return Response(
            {"message": f"{len(speciality_ids)} speciality are successfully deleted."},
            status=status.HTTP_200_OK
        )

def DeleteProcedure(medcent, procedure_pk):
    try: 
        procedure = medcent.procedures.get(id=procedure_pk)
        # name = procedure.name
        procedure.delete()
    except:
        return Response(
                    {"message": "not found"},
                    status=status.HTTP_404_NOT_FOUND
        )

class MedicalCenterProceduresView(APIView):
    def get(self, request, speciality_pk, procedure_pk):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        try:
            procedure = medcent.procedures.filter(id= procedure_pk).first()
        except:
            return Response(
                {"message": "Procedure is not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProcedureSerializer(procedure) # context= {"medcent":medcent}
        return Response( serializer.data, status=status.HTTP_200_OK )

    def delete(self, request, speciality_pk, procedure_pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        if procedure_pk is not None:
            DeleteProcedure(medcent=medcent, procedure_pk=procedure_pk)
            return Response(
                {"message": f"Procedure is successfully deleted."},
                status=status.HTTP_200_OK
            )
        
        procedure_ids = request.data.get("ids", [])
        if not procedure_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for id in procedure_ids:
            DeleteProcedure(medcent=medcent, procedure_pk=id)
        return Response(
            {"message": f"{len(procedure_ids)} procedure are successfully deleted."},
            status=status.HTTP_200_OK
        )


class MedicalCenterHealthInsurancesView(APIView):
    def get(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        try:
            incurances = medcent.contracted_health_institutions.all()
        except:
            return Response(
                {"message": "Contracted Health Insurences are not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = HealthInstitutionsSerializer(incurances, many=True) 
        return Response( serializer.data, status=status.HTTP_200_OK )

    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        serializer = MedicalCenterHealthInstitutionsUpdateSerializer(medcent, data = request.data)
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "New health insurance contraction is successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def delete(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)
        
        # spesific insurance will be deleted
        if pk is not None:
            try: 
                insurance = medcent.contracted_health_institutions.get(id=pk)
                name = insurance.name
                insurance.delete()
                return Response(
                    {"message": f"Contracted Health Insurance {name} is successfully deleted."},
                    status=status.HTTP_200_OK
                )
            except:
                return Response(
                            {"message": "not found"},
                            status=status.HTTP_404_NOT_FOUND
                )
    
        insurance_ids = request.data.get("ids", [])
        if not insurance_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for id in insurance_ids:
                insurance_instance = medcent.contracted_health_institutions.get(id=id)
                insurance_instance.delete()
        return Response(
            {"message": f"{len(insurance_ids)} insurances are successfully deleted."},
            status=status.HTTP_200_OK
        )


class MedicalCenterVideosView(APIView):
    def get(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        try:
            videos = MedicalCenterVideos.objects.filter(medical_center=medcent.id)
        except:
            return Response(
                {"message": "Medical center videos are not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MedicalCenterVideosSerializer(videos, many=True) 
        return Response( serializer.data, status=status.HTTP_200_OK )
    
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, med_cent = getMedicalCenterByID(payload=payload)

        videos = request.data.get("videos", [])
        # {"videos": [{}, {}]}
        for video in videos:
            video['medical_center'] = med_cent.id

            serializer = MedicalCenterVideosSerializer(data=video)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=400)

        response = Response(
            {
                "message": "Videos are successfully added.",
            },
            status=status.HTTP_200_OK
        )
        return response
    
    def delete(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        isTokenValid(token=token)

        if pk is not None:
            try:
                instance = MedicalCenterVideos.objects.get(id=pk)
            except MedicalCenterVideos.DoesNotExist:
                return Response(
                    {"message": "Video is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            video_name = instance.video_name
            instance.delete()
            return Response(
                {"message": f"{video_name} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        video_ids = request.data.get("ids", [])
        if not video_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = MedicalCenterVideos.objects.filter(id__in=video_ids).delete()
        return Response(
            {"message": f"{deleted_count} doctors successfully deleted."},
            status=status.HTTP_200_OK
        )
