from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status

from users.views import *
from medical_centers.serializers import *
from specialities.serializers import SpecialitySerializer
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
        print("hey")
        return response
    


class SpecialityBasedFilteredMedicalCentersView(APIView):
    # this endpoint is redirection endpoint for speciality.views.SpecialityProcedureSelectionView
    # speciality/<int:speciality_id>/<int:procedure_id>
    def get(self, request, speciality_id, procedure_id):

        if speciality_id and procedure_id:
            queryset = MedicalCenter.objects.filter(
                specialities__id=speciality_id,
                procedures__id=procedure_id
            )
        if not queryset.exists():
            return Response(
                {"message": "No medical centers found matching the filters."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicalCenterListSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FilteredMedicalCentersView(APIView):
    # filters : type location speciality procedure

    def get(self, request):
        center_type = request.query_params.get("center_type")
        center_location = request.query_params.get("center_location")
        speciality = request.query_params.get("speciality")
        procedure = request.query_params.get("procedure")

        if center_type or center_location or speciality or procedure:

            queryset = MedicalCenter.objects.all()

            if center_type:
                queryset = queryset.filter(center_type=center_type)
            if center_location:
                queryset = queryset.filter(city=center_location)
            if speciality:
                queryset = queryset.filter(specialities=speciality)
            if procedure:
                queryset = queryset.filter(procedures=procedure)


            if not queryset.exists():
                return Response(
                    {"message": "No medical centers found matching the filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = MedicalCenterListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {"error": "Please provide at least one filter."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        

