# rest framework requirements
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

# db models, serializers and required views
# from users
from users.views import getUserByID, isTokenValid
from users.serializers import UserSerializers
# from specialities
from specialities.serializers import ProcedureSerializer
# from patient
from patient.models import MedicalCenterRequest
from patient.serializers import MedicalCenterRequestSerializer
# from destinations
from destinations.models import Destination
# from inner path
from .models import MedicalCenter, Doctor
from .models import MedicalCenterPhotos, MedicalCenterVideos

from .serializers import MedicalCenterSerializer, MedicalCenterUpdateSerializer
from .serializers import DoctorSerializer
from .serializers import MedicalCenterSpecialitySerializer, MedicalCenterSpecialityUpdateSerializer
from .serializers import HealthInstitutionsSerializer, MedicalCenterHealthInstitutionsUpdateSerializer
from .serializers import MedicalCenterVideosSerializer, MedicalCenterPhotosSerializer

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import redirect



def getMedicalCenterByID(payload:dict) -> tuple:
    """
    Gets MedicalCenter with the ID provided in the payload and returns it.
    
    If any MedicalCenter is not found then raise NotFound (404)

    params:
        payload : dict {'id', 'exp', 'iat'}
    return params:
        tuple (User, MedicalCenter)
            User : object of User Model
            MedicalCenter : object of MedicalCenter Model
    """
    # gets User with users.views.GetUserByID method
    user = getUserByID(payload=payload)
    
    # find MedicalCenter with linked User ID
    # USer model and MedicalCenter model are in OneToOne relation.
    med_cent = MedicalCenter.objects.filter(user=user.id).first()
    if not med_cent:
        raise NotFound("Medical Center not found!")
    return (user, med_cent)
    # return redirect("/users/register")
    
def DeleteSpeciality(medcent:MedicalCenter, specilality_pk:int) -> None|NotFound:
    """
    Deletes the specified specialty and its procedures of the authenticated medical center.
    
    If any Speciality is not found then raise NotFound(404)

    params:
        medcent : object of MedicalCenter
        specilality_pk : ID of the property requested to be deleted
    """
    try: 
        speciality = medcent.specialities.filter(id= specilality_pk).first()

        procedures = medcent.procedures.filter(speciality=specilality_pk)
        if procedures:
            for procedure in procedures:
                procedure.delete()
        speciality.delete()
    except:
        raise NotFound("Speciality is not found!")
   
def DeleteProcedure(medcent:MedicalCenter, procedure_pk:int) -> None|NotFound:
    """
    Deletes the specified Procedure of the authenticated medical center.
    
    If any Procedure is not found then raise NotFound(404)

    params:
        medcent : object of MedicalCenter
        procedure_pk : ID of the property requested to be deleted
    """
    try: 
        procedure = medcent.procedures.get(id=procedure_pk)
        procedure.delete()
    except:
        raise NotFound("Procedure is not found!")
    

class MedicalCenterView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve authenticated medical center profile information.",
        responses={
            200: openapi.Response(
                description="Successful response with user and medical center information.",
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
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!"]
                    }
                )
            ),
        }
    )
    # gets authenticated medical center profile information
    def get(self, request):
        # check token is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        # get MedicalCenter and User object
        user, med_cent = getMedicalCenterByID(payload=payload)
        # serialize their data
        user_serializer = UserSerializers(user)
        med_cent_serializer = MedicalCenterSerializer(med_cent)

        return Response(
            {
            "user": user_serializer.data,
            "med-cent":med_cent_serializer.data  
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
        operation_description = "Updating Whole Medical Center Profile Information. All Data Is Needed!",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the user associated with the medical center."
                ),
                "center_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the medical center."
                ),
                "center_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of the medical center (e.g., Hosp, Clinic)."
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The city name (e.g., İSTANBUL)."
                ),
                "contact_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Contact number of the medical center."
                ),
                "mail_address": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email address of the medical center."
                ),
                "web_site": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Website URL of the medical center."
                ),
                "preview_text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Short description or preview text about the medical center."
                ),
                "overview_text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Detailed description or overview text about the medical center."
                ),
                "specialities": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of speciality IDs associated with the medical center."
                ),
                "procedures": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of procedure IDs offered by the medical center."
                ),
                "contracted_health_institutions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of contracted health institution IDs."
                ),
            },
            required=["__all__"]
        ),
        responses={
            200:openapi.Response(
                description="Medical Center Data Succesfully Updated!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={"message": "Medical Center information is successfully updated.",}
                )
            ),
            400:openapi.Response(
                description="Bad Request!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={"detail": "Medical Center data is not valid!"}
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "City is not found!"]
                    }
                )
            ),
        }
    )
    # used only one time right after registeration for fully updating the whole profile
    # all data is neeeded
    def put(self, request):
        # check if token is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        # get MedicalCenter and User object
        user, med_cent = getMedicalCenterByID(payload=payload)
        # get request data
        data = request.data
        # fix the city 
        try:
            city_object = Destination.objects.filter(name=data["city"]).first()
        except:
            return Response(
                {"detail" : "City is not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data["city"] = city_object.id

        # serialize sent data
        serializer = MedicalCenterUpdateSerializer(med_cent, data=data)
        # if data is valid update object
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

    @swagger_auto_schema(
        operation_description = "Partially Updating Medical Center Profile Information",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "center_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the medical center."
                ),
                "center_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of the medical center (e.g., Hosp, Clinic)."
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="City Name e.g. SAMSUN)."
                ),
                "contact_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Contact number of the medical center."
                ),
                "mail_address": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email address of the medical center."
                ),
                "web_site": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Website URL of the medical center."
                ),
                "preview_text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Short description or preview text about the medical center."
                ),
                "overview_text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Detailed description or overview text about the medical center."
                )
            },
        ),
        responses={
            200:openapi.Response(
                description="Medical Center Data Succesfully Updated!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={"message": "Medical Center information is successfully updated.",}
                )
            ),
            400:openapi.Response(
                description="Bad Request!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={"detail": "Medical Center data is not valid!"}
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "City is not found"]
                    }
                )
            ),
        }
    )
    # will used when updating the profile partially
    def patch(self, request):
        # check token is valid
        token   = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        # get User and MedicalCenter object
        user, med_cent = getMedicalCenterByID(payload=payload)
        # get the data
        data = request.data
        # fix the city 
        try:
            city_object = Destination.objects.filter(name=data["city"]).first()
        except:
            return Response(
                {"detail" : "City is not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data["city"] = city_object.id

        # serialize the data
        # partial parameter is True because user may want to update some of data not all of them
        serializer = MedicalCenterUpdateSerializer(med_cent, data=data, partial=True)

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

    @swagger_auto_schema(
        operation_description="Create doctor records for authenticated medical center.",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Doctor Name"
                ),
                "surname": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Doctor Surname"
                ),
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Doctor Academic Title ('Dr.', 'Prof. Dr.', 'Assoc. Dr.', 'Asst. Dr.')"
                ),
                "major": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Doctor Major Branch"
                ),
                "minor": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Doctor Minor Branch"
                )
            },
            required=["name", "surname", "title", "major"]
        ),
        responses={
            201: openapi.Response(
                description="Doctor Records Successfully Created.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={
                        "message": "Doctors are successfully created."
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Serializer data is invalid.","Please provide at least one doctor info"]
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!"]
                    }
                )
            ),
        }
    )
    # record of one doctor or many doctor
    def post(self, request):
        # check if jwt token is valid 
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        # get User and MedicalCenter
        user, med_cent = getMedicalCenterByID(payload=payload)

        # get request doctors data
        doctors = request.data.get("doctors", [])   
        # {"doctors": [{'name', 'surname', 'title', 'major', 'minor'},]} 
        # minor is optional

        if not doctors:
             return Response(
                    {"detail":"Please provide at least one doctor info"}, 
                    status=status.HTTP_400_BAD_REQUEST)

        for doctor in doctors:
            # Set the related_center field using the retrieved medical center object
            doctor['related_center'] = med_cent.id
            # serialize the data
            doctor_serializer = DoctorSerializer(data=doctor)
            if doctor_serializer.is_valid():
                doctor_serializer.save()
            else:
                return Response(
                    doctor_serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)

        response = Response(
            {
                "message": "Doctors are successfully created.",
            },
            status=status.HTTP_201_CREATED
        )
        return response

    @swagger_auto_schema(
        operation_description="Retrieve authenticated medical center's doctors information list.",
        responses={
            200: openapi.Response(
                description="Successful response with medical center's doctors information list.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'                : openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Doctor ID"),
                            'related_center'    : openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Medical Center ID which doctor works"),
                            'name'              : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Doctor Name"),
                            'surname'           : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Doctor Surname"),
                            'title'             : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Doctor Academic Title"),
                            'major'             : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Doctor Major Branch"),
                            'minor'             : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Doctor Minor Branch if he/she has"),
                        },
                        examples = [
                            {
                                "id": 2,
                                "related_center": 1,
                                "name": "John",
                                "surname": "Doe",
                                "title": "Prof. Dr.",
                                "major": "Aest",
                                "minor": "Anes"
                            }
                        ]
                    )
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "Doctor not found!"]
                    }
                )
            ),
        }
    )
    # get doctors list       
    def get(self, request):
        # check if token is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        # get User and MedicalCenter 
        user, medcent = getMedicalCenterByID(payload=payload)

        # get medical center's doctor
        try:
            doctors = Doctor.objects.filter( related_center = medcent.id )
        except Doctor.DoesNotExist:
            return Response(
                {"detail": "Doctor not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        # serialize the data
        serializer = DoctorSerializer(doctors, many=True)
        return Response( 
            serializer.data, 
            status=status.HTTP_200_OK )

    @swagger_auto_schema(
        operation_description="Delete requested doctors.",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of doctor IDs."
                ),
            },
            required=["ids"]
        ),
        responses={
            200: openapi.Response(
                description="Doctor records successfully deleted.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={
                        "message": "{deletion_count} doctors successfully deleted."
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "No IDs provided for deletion!"
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "No matching records found."]
                    }
                )
            ),
        }
    )
    # delete multiple doctor at once
    def delete(self, request):
        # check if token is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)

        # get User and MedicalCenter, no need return object but we need to sure if the user is medical center 
        getMedicalCenterByID(payload=payload)

        # check if any ids are requested for deletion
        doctor_ids = request.data.get("ids", [])
        if not doctor_ids:
            return Response(
                {"detail": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # filter all requested doctors for deletion
        doctors = Destination.objects.filter(id__in=doctor_ids)
        if not doctors.exists():
            return Response(
                {"detail": "No matching records found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # delete them
        count, _ = doctors.delete() 
        return Response(
            {"message": f"{count} doctors successfully deleted."},
            status=status.HTTP_200_OK,
        )


class MedicalCenterDoctorView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve authenticated medical center's requested doctor information",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the requested Doctor",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful response with medical center's requested doctor information.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id'                : openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Doctor ID"),
                        'related_center'    : openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Medical Center ID which doctor works"),
                        'name'              : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Name"),
                        'surname'           : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Surname"),
                        'title'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Academic Title"),
                        'major'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Major Branch"),
                        'minor'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Minor Branch if he/she has"),
                    },
                    examples = {
                            "id": 2,
                            "related_center": 1,
                            "name": "John",
                            "surname": "Doe",
                            "title": "Prof. Dr.",
                            "major": "Aest",
                            "minor": "Anes"
                        }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "Doctor not found!"]
                    }
                )
            ),
        }
    )
    # get requested doctor 
    def get(self, request, id):

        # check if token and users are valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        getMedicalCenterByID(payload=payload)
        # get requested Doctor instance
        try:
            instance = Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            return Response(
                {"detail": "Doctor not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        # serialize the data then send
        serializer = DoctorSerializer(instance)
        return Response( serializer.data, status=status.HTTP_200_OK )
    
    @swagger_auto_schema(
        operation_description="Update authenticated medical center's requested doctor information partially",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the requested Doctor",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name'              : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Name"),
                        'surname'           : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Surname"),
                        'title'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Academic Title ('Dr.', 'Prof. Dr.', 'Assoc. Dr.', 'Asst. Dr.')"),
                        'major'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Major Branch"),
                        'minor'             : openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Doctor Minor Branch if he/she has"),
                    },
                    examples = {
                            "name": "John",
                            "surname": "Doe",
                            "title": "Prof. Dr.",
                            "major": "Aest",
                            "minor": "Anes"
                        }
                ),
        responses={
            200: openapi.Response(
                description="Doctor information succesfully updated!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={"message" : "Doctor information is succesfully updated."}
                )
            ),
            400: openapi.Response(
                description="Bad Request!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Serializer data is invalid."]
                    }
                )
            ),        
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "Doctor not found!"]
                    }
                )
            ),
        }
    )
    # update requested doctor partially
    def patch(self, request, id):
        # check if token and user are valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        getMedicalCenterByID(payload=payload)
        # get requested doctor 
        try:
            doctor = Doctor.objects.get(id=id) 
        except Doctor.DoesNotExist:
            return Response(
                {"detail": "Doctor not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
    
        if serializer.is_valid():
            serializer.save() 
            return Response(
                {"message" : "Doctor information is succesfully updated."}, 
                status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete authenticated medical center's requested doctor",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the requested Doctor",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Succesfully deleted authenticated medical center's requested doctor.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={"message": "{doctor_name} is successfully deleted."}
                )
            ),           
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "Doctor not found!"]
                    }
                )
            ),
        }
    )
    # delete requested doctor 
    def delete(self, request, id):
        # check if token and user is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        getMedicalCenterByID(payload)
        # get requested doctor
        try:
            instance = Doctor.objects.get(id=id)
        except Doctor.DoesNotExist:
            return Response(
                {"detail": "Doctor not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        name = f"{instance.title} {instance.name} {instance.surname}"
        # delete the doctor
        instance.delete()
        return Response(
            {"message": f"{name} is successfully deleted."},
            status=status.HTTP_200_OK
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

    @swagger_auto_schema(
        operation_description="Retrieve authenticated medical center's contracted health insurances list.",
        responses={
            200: openapi.Response(
                description="Successful response with medical center's contracted health insurances list.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id'                : openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Health Insurance ID"),
                            'name'              : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Health Insurance Name"),
                            'code'           : openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Health Insurance Code")
                        },
                        examples = [
                           {
                                "id": 2,
                                "name": "Allianz Sigorta",
                                "code": " Allianz"
                            },
                        ]
                    )
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "Contracted Health Insurences are not found!"]
                    }
                )
            ),
        }
    )
    # get medical center contracted health insurances list
    def get(self, request):
        # check if token and user is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)
        # get all contracted health insurances list
        try:
            incurances = medcent.contracted_health_institutions.all()
        except:
            return Response(
                {"detail": "Contracted Health Insurences are not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        # serialize the data
        serializer = HealthInstitutionsSerializer(incurances, many=True) 
        return Response( serializer.data, status=status.HTTP_200_OK )

    @swagger_auto_schema(
        operation_description="Create new health insurances contract for authenticated medical center.",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "contracted_health_institutions": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Health Insurance Object's ID's"
                )
            },
            required=["contracted_health_institutions"]
        ),
        responses={
            200: openapi.Response(
                description="Successfully created new health insurance record for authenticated medical center.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={"message": "New health insurance contraction is successfully added."}
                )
            ),
            400: openapi.Response(
                description="Bad Request!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Health Insurance data is not valid!"
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!"]
                    }
                )
            ),
        }
    )
    # create new insurance contract record
    def post(self, request):
        # check if token and user is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)
        # serialize the request data
        serializer = MedicalCenterHealthInstitutionsUpdateSerializer(medcent, data = request.data)
        # if valid then save
        if serializer.is_valid():
                serializer.save()
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": "New health insurance contraction is successfully added.",
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
        operation_description="Delete requested contracted health insurance record.",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of health insurance IDs."
                ),
            },
            required=["ids"]
        ),
        responses={
            200: openapi.Response(
                description="Contracted health insurance records successfully deleted.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={
                        "message": "{deletion_count} contracted health insurance successfully deleted."
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "No IDs provided for deletion!"
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "No matching records found."]
                    }
                )
            ),
        }
    )
    # delete requested multiple health insurance records at once
    def delete(self, request):
        # check if token or user is valid
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        # get requested health insurance ids for deletion
        insurance_ids = request.data.get("ids", [])
        # check if any ids are requested for deletion
        if not insurance_ids:
            return Response(
                {"detail": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # filter all requested doctors for deletion
        insurances = medcent.contracted_health_institutions.filter(id__in=insurance_ids)
        if not insurances.exists():
            return Response(
                {"detail": "No matching records found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # delete them
        count, _ = insurances.delete()
        return Response(
            {"message": f"{count} contracted health insurance are successfully deleted."},
            status=status.HTTP_200_OK
        )


class MedicalCenterHealthInsuranceView(APIView):
    @swagger_auto_schema(
        operation_description="Delete requested contracted health insurance record.",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="List of health insurance IDs."
                ),
            },
            required=["ids"]
        ),
        responses={
            200: openapi.Response(
                description="Contracted health insurance records successfully deleted.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    },
                    example={
                        "message": "{deletion_count} contracted health insurance successfully deleted."
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "No IDs provided for deletion!"
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication Failed!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Invalid or expired token!"
                    }
                )
            ),
            404: openapi.Response(
                description="Not Found!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": ["Authentication token is missing.", "Medical Center not found!", "User is not found!", "No matching records found."]
                    }
                )
            ),
        }
    )
    # delete requested multiple health insurance records at once
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


class MedicalCenterPhotosView(APIView):
    def get(self, request, pk=None):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, medcent = getMedicalCenterByID(payload=payload)

        try:
            photos = MedicalCenterPhotos.objects.filter(medical_center=medcent.id)
        except:
            return Response(
                {"message": "Medical center photos are not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MedicalCenterPhotosSerializer(photos, many=True) 
        return Response( serializer.data, status=status.HTTP_200_OK )
    
    def post(self, request):
        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        user, med_cent = getMedicalCenterByID(payload=payload)

        photos = request.FILES.getlist('photos', [])  
        errors = []

        for photo in photos:
            photo_data = {
                'medical_center': med_cent.id,
                'image_name': photo.name,  
                'image': photo, 
            }
            serializer = MedicalCenterPhotosSerializer(data=photo_data)

            if serializer.is_valid():
                serializer.save()
            else:
                errors.append({"photo": photo, "errors": serializer.errors})

        if errors:
            return Response({"errors": errors}, status=400)

        return Response(
            {"message": "Photos are successfully added."},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, pk):

        token = request.COOKIES.get("jwt")
        isTokenValid(token=token)

        if pk is not None:
            try:
                photo = MedicalCenterPhotos.objects.get(id=pk)
            except MedicalCenterVideos.DoesNotExist:
                return Response(
                    {"message": "Video is not found!"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if photo.image:
                file_path = photo.image.path
                if os.path.exists(file_path):
                    os.remove(file_path)  
                image_name = photo.image_name
                photo.delete()

            return Response(
                {"message": f"Image {image_name} is successfully deleted."},
                status=status.HTTP_200_OK
            )

        image_ids = request.data.get("ids", [])
        if not image_ids:
            return Response(
                {"message": "No IDs provided for deletion!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_count, _ = MedicalCenterPhotos.objects.filter(id__in=image_ids).delete()
        return Response(
            {"message": f"{deleted_count} doctors successfully deleted."},
            status=status.HTTP_200_OK
        )
    

class MedicalCenterRequestsView(APIView):
    def get(self, request):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, medcent = getMedicalCenterByID(payload=payload)
        # get medical center's requests
        try:
            requests = MedicalCenterRequest.objects.filter( medical_center = medcent.id )
        except:
            return Response (
                {
                    "message" : "Requests are not found!" 
                },
                status = status.HTTP_404_NOT_FOUND
            )
    
        serializer = MedicalCenterRequestSerializer(requests, many = True)

        return Response(
                    {
                        "requests" : serializer.data,
                    },
                    status=status.HTTP_200_OK
                )   

class FilteredMedicalCenterRequestsView(APIView):
    def get(self, request):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, medcent = getMedicalCenterByID(payload=payload)

        speciality = request.query_params.get("speciality")
        procedure = request.query_params.get("procedure")

        if speciality or procedure:

            queryset = MedicalCenterRequest.objects.filter( medical_center = medcent.id )

            if speciality:
                queryset = queryset.filter(speciality=speciality)
            if procedure:
                queryset = queryset.filter(procedure=procedure)


            if not queryset.exists():
                return Response(
                    {"message": "No request found matching the filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = MedicalCenterRequestSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {"error": "Please provide at least one filter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
