# rest framework dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# db models and their serializers
from medical_centers.models import Speciality
from .serializers import SpecialitySerializer

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import redirect

"""
specialities view.py file contains all speciality list endpoint and speciality-procedure selection endpoint
SpecialitiesView get api is return all speciality list with their procedures
SpecialityProcedureSelectionView get is redrect to /medical-centers/{speciality_id}/{procedure_id} url 

each function is explained with swagger and comment block
"""


class SpecialitiesView(APIView):
    @swagger_auto_schema(
        operation_description="Specialities List Endpoint, (no need to authentication)",
        responses={
            200: openapi.Response(
                description="Specialities List Successfully Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'code': openapi.Schema(type=openapi.TYPE_STRING),
                            'procedures': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'code': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                )
                            )
                        }
                    ),
                    example=[
                                {
                                    "id": 58,
                                    "name": "Addiction Treatment",
                                    "code": "AT",
                                    "procedures": [
                                        {
                                            "id": 2,
                                            "name": "Alcohol addiction treatment",
                                            "code": "AT-1"
                                        },
                                        {
                                            "id": 3,
                                            "name": "Drug addiction treatment",
                                            "code": "AT-2"
                                        },
                                    ]
                                }
                            ]
                )
            ),
            404: openapi.Response(
                description="Speciality not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Not found any speciality record!"
                    }
                )
            )
        }
    )
    def get(self, request):
        # no need to login

        try: 
            # get all specialities record from db
            specialities = Speciality.objects.all()
        except:
            # if any error occurs response with not found
            return Response(
                {"detail": "Not found any speciality record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        # serialize the data for jsonification
        serializer = SpecialitySerializer(specialities, many= True)
        # prepare response data
        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response

    
class SpecialityProcedureSelectionView(APIView):
    @swagger_auto_schema(
        operation_description="""After speciality-procedure selection, url redirect to medical-centers list filtered with selected speciality and procedure.
        specialities/speciality_id/procedure_id -> medical-centers/speciality_id/procedure_id
        (no need to authentication)""",
        
        responses={
            200: openapi.Response(
                description="Redirects to the medical center endpoint.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='path')
                    },
                    example={
                        'location': '/medical-centers/1/2'  
                    }
                )
            ),
            400: openapi.Response(
                description="Speciality and procedure ID is not provided.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error details')
                    },
                    example={
                        'detail': 'Speciality and procedure not provided.'
                    }
                )
            )
        }
    )
    def get(self, request, speciality_id:int, procedure_id:int):

        # if url parameters exist 
        if speciality_id and procedure_id:
            # redirect to medical-centers list view which is medical centers filtered with specified speciality and procedure 
            # centers.urls -> medical-centers/<int:speciality_id>/<int:procedure_id> (SpecialityBasedFilteredMedicalCentersView)
            new_url = f"/medical-centers/{speciality_id}/{procedure_id}"
            return redirect(new_url)
        
        return Response(
            {"detail": "Speciality and procedure not provided."},
            status=status.HTTP_400_BAD_REQUEST
        )