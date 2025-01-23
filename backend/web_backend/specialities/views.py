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
            specialities = Speciality.objects.all()
        except:
            return Response(
                {"detail": "Not found any speciality record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = SpecialitySerializer(specialities, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response

    

class SpecialityProcedureSelectionView(APIView):
    @swagger_auto_schema(
        operation_description="After speciality-procedure selection, url redirect to medical-center filtered with selected speciality and procedure (no need to authentication)",
        operation_id='speciality_procedure_selection',  # Optional: Give a unique ID to this operation
        
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
    def get(self, request, speciality_id, procedure_id):

        if speciality_id and procedure_id:
            new_url = f"/medical-centers/{speciality_id}/{procedure_id}"
            return redirect(new_url)
        
        return Response(
            {"detail": "Speciality and procedure not provided."},
            status=status.HTTP_400_BAD_REQUEST
        )