# rest framework dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# db models, their serializers and views
from users.views import isTokenValid
from patient.views import getPatientByID
from medical_centers.serializers import MedicalCenterSerializer
from .serializers import MedicalCenterListSerializer
from medical_centers.models import MedicalCenter

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import redirect

"""
centers views.py file contains 
    all medical center preview list endpoints, 
    specific medical center overview endpoints
    redirect endpoint for specific medical center request
    speciality-prcedure selected medical center preview list endpoints
    and lastly filtered medical center preview list endpoints

No endpoint requires authentication except MedicalCentersByIDView POST method

each function is explained with swagger and comment block
"""


class MedicalCentersView(APIView):
    @swagger_auto_schema(
        operation_description="Medical Center List Endpoint, (no need to authentication)",
        responses={
            200: openapi.Response(
                description="Medical Center List Successfully Created",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                            'center_name'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'center_type'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'city'          : openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'id'    : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                    'name'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                }                         
                           ),
                            'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'mail_address'  : openapi.Schema(type=openapi.TYPE_STRING),
                            'web_site'      : openapi.Schema(type=openapi.TYPE_STRING),
                            'preview_text'  : openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                    example=[
                                {
                                    "id": 1,
                                    "center_name": "Awesome Medical Center",
                                    "center_type": "Hosp",
                                    "city": {
                                        "id": 1,
                                        "city": "İSTANBUL"
                                    },
                                    "contact_number": "+905555555555",
                                    "mail_address": "info@medicalcenter.com",
                                    "web_site": "https://medicalcenter.com",
                                    "preview_text": "Short about us.."
                                }
                            ]
                )
            ),
            404: openapi.Response(
                description="Medical Centers not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Not found any medical center record!"
                    }
                )
            )
        }
    )
    # return all medical centers list
    def get(self, request):

        # no need to login
        try: 
            # get all medical center records from db
            medcents = MedicalCenter.objects.all()
        except:
            return Response(
                {"detail": "Not found any medical center record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        # serialize the data for jsonification
        serializer = MedicalCenterListSerializer(medcents, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response


class MedicalCentersByIDView(APIView):
    @swagger_auto_schema(
        operation_description="Medical Center Overview Endpoint, (no need to authentication)",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the medical center",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Gets Medical Center Overview With Provided ID",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                            'center_name'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'center_type'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'city'          : openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'id'    : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                    'name'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                }                         
                           ),
                            'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'mail_address'  : openapi.Schema(type=openapi.TYPE_STRING),
                            'web_site'      : openapi.Schema(type=openapi.TYPE_STRING),
                            'preview_text'  : openapi.Schema(type=openapi.TYPE_STRING),
                            'overview_text' : openapi.Schema(type=openapi.TYPE_STRING),
                            'specialities'  : openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        'id'    : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                        'name'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                        'code'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                        'procedures': openapi.Schema(
                                                            type=openapi.TYPE_ARRAY,
                                                            items=openapi.Schema(
                                                                type=openapi.TYPE_OBJECT,
                                                                properties={
                                                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                                    'specialitiy': openapi.Schema(type=openapi.TYPE_INTEGER)
                                                                }
                                                            )
                                                        )
                                                    }
                                                )
                                            ),
                            'contracted_health_institutions': openapi.Schema(
                                                                type=openapi.TYPE_ARRAY,
                                                                items=openapi.Schema(
                                                                    type=openapi.TYPE_OBJECT,
                                                                    properties={
                                                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'code': openapi.Schema(type=openapi.TYPE_STRING)
                                                                    }
                                                                )
                                                            ),
                            'doctors'       : openapi.Schema(
                                                                type=openapi.TYPE_ARRAY,
                                                                items=openapi.Schema(
                                                                    type=openapi.TYPE_OBJECT,
                                                                    properties={
                                                                        'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                        'related_center': openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'name'          : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'surname'       : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'title'         : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'major'         : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'minor'         : openapi.Schema(type=openapi.TYPE_STRING),
                                                                    }
                                                                )
                                                            ),
                            'medical_center_photos'         : openapi.Schema(
                                                                type=openapi.TYPE_ARRAY,
                                                                items=openapi.Schema(
                                                                    type=openapi.TYPE_OBJECT,
                                                                    properties={
                                                                        'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                        'image_name'    : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'image'         : openapi.Schema(type=openapi.TYPE_STRING, description="Full Image Path, (/media/mdical_center/<int:id>/photos/<str:imageName.fileExtension>)"),
                                                                        'uploaded_at'   : openapi.Schema(type=openapi.TYPE_STRING)
                                                                    }
                                                                )
                                                            ),
                            'medical_center_videos'         : openapi.Schema(
                                                                type=openapi.TYPE_ARRAY,
                                                                items=openapi.Schema(
                                                                    type=openapi.TYPE_OBJECT,
                                                                    properties={
                                                                        'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                        'video_name'    : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'video_link'    : openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'uploaded_at'   : openapi.Schema(type=openapi.TYPE_STRING)
                                                                    }
                                                                )
                                                            )
                        }
                    ),
                    example={
                            "id": 1,
                            "center_name": "Awesome Medical Center",
                            "center_type": "Hosp",
                            "city": {
                                "id": 1,
                                "city": "İSTANBUL"
                            },
                            "contact_number": "+905555555555",
                            "mail_address": "info@medicalcenter.com",
                            "web_site": "https://medicalcenter.com",
                            "preview_text": "Short about us..",
                            "overview_text": "Details about the medical center...",
                            "specialities": [
                                {
                                    "id": 60,
                                    "name": "Allergy",
                                    "code": "All",
                                    "procedures": [
                                        {
                                            "id": 31,
                                            "name": "Atopic dermatitis",
                                            "code": "All-3",
                                            "speciality": 60
                                        }
                                    ]
                                }
                            ],
                            "contracted_health_institutions": [
                                {
                                    "id": 2,
                                    "name": "Allianz Sigorta",
                                    "code": " Allianz"
                                }
                            ],
                            "doctors": [
                                {
                                    "id": 2,
                                    "related_center": 1,
                                    "name": "ahmet",
                                    "surname": "necip",
                                    "title": "Prof. Dr.",
                                    "major": "Aest",
                                    "minor": "Anes"
                                }
                            ],
                            "medical_center_photos": [
                                {
                                    "id": 2,
                                    "image_name": "almondblossoms.jpeg",
                                    "image": "/media/medical_center/1/photos/3b14d0e2-cc74-485d-a8c0-f8d1fbc3601d.jpeg",
                                    "uploaded_at": "2025-01-24T12:13:38.329275Z"
                                }
                            ],
                            "medical_center_videos": [
                                {
                                    "id": 3,
                                    "video_name": "video-1.mp4",
                                    "video_link": "https://www.youtube.com/watch?v=qrBWZ8ARD_s",
                                    "uploaded_at": "2025-01-16T15:40:14.550713Z"
                                }
                            ]
                        }
                )
            ),
            404: openapi.Response(
                description="Medical Center not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Medical center is not found!",
                        "detail": "Please provide a medical center ID."
                    }
                )
            )
        }
    )
    # get medical center belongs to the provided id
    def get(self, requests, id):
        if id is not None:
            try: 
                medcent = MedicalCenter.objects.get(id=id)
            except:
                return Response(
                    {"detail": "Medical center is not found!"},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = MedicalCenterSerializer(medcent)

            response = Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
            return response
        else:
            return Response(
                    {"detail": "Please provide a medical center ID."},
                    status = status.HTTP_404_NOT_FOUND
                )
    
    @swagger_auto_schema(
        operation_description="Redirect to the url /patient/medical-center-request/{id}/",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the medical center",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            302: openapi.Response(
                description="Successfully redirected to the new URL."
                ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token.",
                        "detail": "Need to be patient profile!"
                    }
                )
            ),
            404: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Patient not found!"
                    }
                )
            )

        }
    )
    # this endpoint is for redirection
    # if user is patient then this view redirect to the url patient/medical-center-request/id with the ID of current medical center
    def post(self, request, id):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)

        if patient:
            new_url = f"/patient/medical-center-request/{id}/"
            return redirect(new_url)
        else:
            return Response(
                {"detail": "Need to be patient profile!",},
                status=status.HTTP_401_UNAUTHORIZED
            )


class SpecialityBasedFilteredMedicalCentersView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of medical centers based on speciality and procedure filters.",
        manual_parameters=[
            openapi.Parameter(
                'speciality_id',
                openapi.IN_PATH,
                description="ID of the speciality to filter medical centers.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'procedure_id',
                openapi.IN_PATH,
                description="ID of the procedure to filter medical centers.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="List of medical centers matching the filters.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                            'center_name'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'center_type'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'city'          : openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'id'    : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                    'name'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                }                         
                           ),
                            'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'mail_address'  : openapi.Schema(type=openapi.TYPE_STRING),
                            'web_site'      : openapi.Schema(type=openapi.TYPE_STRING),
                            'preview_text'  : openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                    example=[
                                {
                                    "id": 1,
                                    "center_name": "Awesome Medical Center",
                                    "center_type": "Hosp",
                                    "city": {
                                        "id": 1,
                                        "city": "İSTANBUL"
                                    },
                                    "contact_number": "+905555555555",
                                    "mail_address": "info@medicalcenter.com",
                                    "web_site": "https://medicalcenter.com",
                                    "preview_text": "Short about us.."
                                }
                            ]
                )
            ),
            404: openapi.Response(
                description="No medical centers found matching the filters.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "No medical centers found matching the filters."
                    }
                )
            )
        }
    )
    # this endpoint is end of the redirection endpoint for speciality.views.SpecialityProcedureSelectionView
    # specialities/<int:speciality_id>/<int:procedure_id> -> medical-centers/<int:speciality_id>/<int:procedure_id>
    def get(self, request, speciality_id:int, procedure_id:int)->Response:

        # if speciality and procedure id is provided
        if speciality_id and procedure_id:
            try:
                # retrieve the medical centers with the filter of these ID's
                queryset = MedicalCenter.objects.filter(
                    specialities__id=speciality_id,
                    procedures__id=procedure_id
                )
            except:
                return Response(
                    {"detail": "No medical centers found matching the filters."},
                    status=status.HTTP_404_NOT_FOUND
                )
        # serialize the data
        serializer = MedicalCenterListSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FilteredMedicalCentersView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of medical centers based on the provided filters.",
        manual_parameters=[
            openapi.Parameter(
                'center_type',
                openapi.IN_QUERY,
                description="Type of the medical center ('Hosp', 'Clin', 'MedCent', 'UniHosp', 'DentClin', 'UniMedCent', 'Cent', 'HospGrp', 'RehabCent', 'ChildCent').",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'center_location',
                openapi.IN_QUERY,
                description="ID of the city where the medical center is located.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'speciality',
                openapi.IN_QUERY,
                description="Speciality ID to filter medical centers.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'procedure',
                openapi.IN_QUERY,
                description="Procedure ID to filter medical centers.",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of medical centers matching the filters.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'            : openapi.Schema(type=openapi.TYPE_INTEGER),
                            'center_name'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'center_type'   : openapi.Schema(type=openapi.TYPE_STRING),
                            'city'          : openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'id'    : openapi.Schema(type=openapi.TYPE_INTEGER),
                                                    'name'  : openapi.Schema(type=openapi.TYPE_STRING),
                                                }                         
                           ),
                            'contact_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'mail_address'  : openapi.Schema(type=openapi.TYPE_STRING),
                            'web_site'      : openapi.Schema(type=openapi.TYPE_STRING),
                            'preview_text'  : openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                    example=[
                                {
                                    "id": 1,
                                    "center_name": "Awesome Medical Center",
                                    "center_type": "Hosp",
                                    "city": {
                                        "id": 1,
                                        "city": "İSTANBUL"
                                    },
                                    "contact_number": "+905555555555",
                                    "mail_address": "info@medicalcenter.com",
                                    "web_site": "https://medicalcenter.com",
                                    "preview_text": "Short about us.."
                                }
                            ]
                )
            ),
            404: openapi.Response(
                description="No medical centers found matching the filters.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    },
                    example={
                        "message": "No medical centers found matching the filters."
                    }
                )
            ),
            400: openapi.Response(
                description="No filters provided in the query parameters.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    },
                    example={
                        "error": "Please provide at least one filter."
                    }
                )
            )
        }
    )
    # Retrieve a list of medical centers filtered by type, location, speciality, or procedure.
    def get(self, request):

        # get query params
        center_type = request.query_params.get("center_type")
        center_location = request.query_params.get("center_location")
        speciality = request.query_params.get("speciality")
        procedure = request.query_params.get("procedure")
        # if any query param is provided
        if center_type or center_location or speciality or procedure:

            queryset = MedicalCenter.objects.all()
            # filter the medical center record with the parameters
            if center_type:
                queryset = queryset.filter(center_type=center_type)
            if center_location:
                queryset = queryset.filter(city=center_location)
            if speciality:
                queryset = queryset.filter(specialities=speciality)
            if procedure:
                queryset = queryset.filter(procedures=procedure)


            if (not queryset.exists()) or (queryset is []):
                return Response(
                    {"message": "No medical centers found matching the filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # if there is any record then serialize the data
            serializer = MedicalCenterListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {"error": "Please provide at least one filter."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        

