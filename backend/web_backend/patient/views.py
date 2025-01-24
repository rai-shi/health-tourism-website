# rest framework dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# db models, their serializers and views
from .serializers import PatientSerializers, MedicalCenterRequestSerializer, MedicalCenterRequestViewSerializer
from .models import Patient, MedicalCenterRequest
from users.serializers import UserSerializers
from users.views import getUserByID, isTokenValid

from cities_light.models import City, Country

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


"""
patient views.py file contains endpoints for profile, medical center request viewing and endpoints for sending request to medical centers

and patient-spesific services are
getPatientByID gets patient with the id provided in JWT Token Payload

each function is explained with swagger and comment block
"""


def getPatientByID(payload:dict)->tuple:
    """
    Gets Patient with the ID provided in the payload and returns it.
    
    If any Patient is not found then returns 404 Response

    params:
        payload : dict {'id', 'exp', 'iat'}
    return params:
        tuple (User, Patient)
            User : object of User Model
            Patient : object of Patient Model
    """
    # gets User with users.views.GetUserByID method
    user = getUserByID(payload=payload)

    # find Patient with linked User ID
    # USer model and Patient model are in OneToOne relation.
    patient = Patient.objects.filter(user=user.id).first()
    if not patient:
        return Response(
                {"detail": "Patient not found!"},
                status= status.HTTP_404_NOT_FOUND
            )
    
    return (user, patient)
    

# GET, POST
class PatientView(APIView):
    @swagger_auto_schema(
        operation_description= "Gets patient user profile information endpoint",
        # no request body only need token in COOKIES
        responses={
            200: openapi.Response(
                description="Patient user profile data successfuly fetched.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user' :openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        ),
                        'patient': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                                'birthday': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                'country': openapi.Schema(type=openapi.TYPE_STRING),
                                'city': openapi.Schema(type=openapi.TYPE_STRING),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    },
                    example={
                        "user": {
                            "first_name": "ayse",
                            "last_name": "tak",
                            "email": "ayse1@gmail.com",
                            "is_staff": False
                        },
                        "patient": {
                            "gender": "w",
                            "birthday": "2000-02-07",
                            "phone_number": "+905323936604",
                            "country": "Turkey",
                            "city": "Samsun, Samsun, Turkey",
                            "created_at": "2025-01-14T14:55:16.361336Z"
                        }
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
    # patient profile information get endpoint
    def get(self, request):
        token = request.COOKIES.get("jwt")
        # check token is valid or expired
        payload = isTokenValid(token=token)

        # take user and its patient record from payload
        user, patient = getPatientByID(payload=payload)

        # make the data json valid
        user_serializer = UserSerializers(user)
        patient_serializer = PatientSerializers(patient)

        response = Response(
            {
                "user": user_serializer.data,
                "patient":patient_serializer.data 
            },
            status=status.HTTP_200_OK
        )
        return response
    
    @swagger_auto_schema(
        operation_description="User profile information update endpoint",
        responses= {
            201: openapi.Response(
                description="Patient user profile data successfuly updated.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'birthday': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'country': openapi.Schema(type=openapi.TYPE_STRING),
                        'city': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    example={
                        "gender": "w",
                        "birthday": "2000-02-07",
                        "phone_number": "+905323936604",
                        "country": "TR",
                        "city": "Samsun",                          
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
    # patient profile information update endpoint
    def post(self, request):

        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)

        # get country and city data and fix them for serializer
        country         = request.data.get("country")
        city            = request.data.get("city")
        # Assume that country codes are got -> For Turkey, TR is got.
        try:
            city_object = City.objects.filter(name=city).first()
            country_object = Country.objects.filter(code2=country).first()
        except Exception as e:
            return Response(
                {"detail" : f"{e}"},
                status=status.HTTP_404_NOT_FOUND
            )
        # prepare serializer data
        data = request.data 
        data["city"] = city_object
        data["country"] = country_object

        # serialize the data and if its valid then save
        serializer = PatientSerializers(patient, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

        response = Response(
            {
                "message": "Personal information is successfully updated.",
            },
            status=status.HTTP_200_OK
        )
        return response
  

# GET, POST
class RequestsView(APIView):
    @swagger_auto_schema(
        operation_description="Creates a new medical center request.",
        request_body= openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'medical_center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Medical Center ID'),
                'speciality': openapi.Schema(type=openapi.TYPE_INTEGER, description='Speciality ID'),
                'procedure': openapi.Schema(type=openapi.TYPE_INTEGER, description='Procedure ID'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Name'),
                'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Patinet Surname'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Gender'),
                'birthday': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Birthday'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Phone Number'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Email'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Country Code'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='Patient City Name'),
                'disease_history': openapi.Schema(type=openapi.TYPE_STRING, description='Patient disease history as a text'),
                'previous_disease': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous disease as a text'),
                'previous_surgery': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous surgery as a text'),
                'previous_treatment': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous treatment as a text'),
                'other_comments': openapi.Schema(type=openapi.TYPE_STRING, description="Patient' other comments as a text"),
            },
            required=["__all__"],
            example={
                "medical_center"  : 1,
                "speciality"      : 62,
                "procedure"       : 43,
                "name"            : "John",
                "surname"         : "Doe",
                "gender"        : "m",
                "birthday"      : "2000-2-7",
                "phone"         : "+901234567890",
                "email"         : "example@gmail.com",
                "country"       : "TR",
                "city"          : "Samsun",
                "disease_history"     : "Started on five months ago.",
                "previous_disease"    : "-",
                "previous_surgery"    : "-",
                "previous_treatment"  : "-",
                "other_comments"      : "-"
            }
        ),
        responses={
            200: openapi.Response(
                description="Medical Center request is successfully created.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Success message."
                        ),
                    },
                    example={
                        "message": "Medical Center request is successfully created.",
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
                        "detail": "Request data is invaild."
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
    # creates new requests for medical center
    def post(self, request):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)

        # get request data
        data = request.data
        # append patient id to data
        data['patient'] = patient.id 
        # fix the city and country data
        city_object = City.objects.filter(name=data["city"]).first()
        country_object = Country.objects.filter(code2=data["country"]).first() 
        data["city"] = city_object.id
        data["country"] = country_object.id
        # serialize the data
        serializer = MedicalCenterRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "message": "Medical Center request is successfully created.",
                },
                status=status.HTTP_200_OK
            )   
            return response
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Gets patient's all medical center requests list.",
        responses={
            200: openapi.Response(
                description="Patient's all requests data successfuly fetched.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'requests' :openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'medical_center': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                                'speciality': openapi.Schema(type=openapi.TYPE_STRING),
                                'procedure': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    },
                    example={
                        "requests": [
                            {
                                "id": 1,
                                "medical_center": 1,
                                "created_at": "01/20/2025, 11:47:20",
                                "speciality": "Allergy",
                                "procedure": "Food allergy"
                            },
                            {
                                "id": 9,
                                "medical_center": 1,
                                "created_at": "01/22/2025, 12:00:34",
                                "speciality": "Bariatrics",
                                "procedure": "Gastric banding"
                            },
                        ]
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
                        "detail": "Patient not found!",
                        "detail" : "Requests are not found!" 
                    }
                )
            )
        }
    )
    # gets all medical center requests list
    def get(self, request):
        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)

        user, patient = getPatientByID(payload=payload)
        # get patient's requests
        try:
            instance = MedicalCenterRequest.objects.filter( patient = patient.id )
        except:
            return Response (
                {
                    "detail" : "Requests are not found!" 
                },
                status = status.HTTP_404_NOT_FOUND
            )
        # make data json valid
        serializer = MedicalCenterRequestViewSerializer(instance, many = True)

        # this endpoint sends only data for listing 
        # if any request is clicked then all request information will be displayed
        # so we need to prepare data
        requests = []
        for request in serializer.data:
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
    @swagger_auto_schema(
        operation_description="Gets patient's specified medical center request information.",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the medical center request",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Patient's specified request data successfuly fetched.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Request ID"),
                        'patient': openapi.Schema(type=openapi.TYPE_INTEGER, description="Patient ID"),
                        'medical_center': openapi.Schema(type=openapi.TYPE_INTEGER, description="Medical Center ID"),
                        'speciality': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id":openapi.Schema(type=openapi.TYPE_INTEGER, description="Speciality ID"),
                                "name":openapi.Schema(type=openapi.TYPE_STRING, description="Speciality Name"),
                            }
                        ),
                        'procedure': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id":openapi.Schema(type=openapi.TYPE_INTEGER, description="Procedure ID"),
                                "name":openapi.Schema(type=openapi.TYPE_STRING, description="Procedure Name"),
                            }
                        ),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Name'),
                        'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Patinet Surname'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Gender'),
                        'birthday': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Birthday'),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Phone Number'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Email'),
                        'country': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Country Code'),
                        'city': openapi.Schema(type=openapi.TYPE_STRING, description='Patient City Name'),
                        'disease_history': openapi.Schema(type=openapi.TYPE_STRING, description='Patient disease history as a text'),
                        'previous_disease': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous disease as a text'),
                        'previous_surgery': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous surgery as a text'),
                        'previous_treatment': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous treatment as a text'),
                        'other_comments': openapi.Schema(type=openapi.TYPE_STRING, description="Patient' other comments as a text"),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description="Request creation date"),
                    },
                    example={
                        "id": 1,
                        "patient": 2,
                        "medical_center": 1,
                        "speciality": {
                            "id": 60,
                            "name": "Allergy"
                        },
                        "procedure": {
                            "id": 33,
                            "name": "Food allergy"
                        },
                        "name": "Ayse",
                        "surname": "Tak",
                        "gender": "w",
                        "birthday": "2000-02-07",
                        "phone": "+905323936604",
                        "email": "aysenurtak1@gmail.com",
                        "country": "Turkey",
                        "city": "Samsun",
                        "disease_history": "Started on five months ago.",
                        "previous_disease": "-",
                        "previous_surgery": "-",
                        "previous_treatment": "-",
                        "other_comments": "-",
                        "created_at": "01/20/2025, 11:47:20"
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
                        "detail": "Patient not found!",
                        "detail" : "Request is not found!" 
                    }
                )
            )
        }
    )
    # gets specified medical center requests
    def get(self, request, id):
        token = request.COOKIES.get("jwt")
        isTokenValid(token=token)

        # get specified patient's request
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
    @swagger_auto_schema(
        operation_description="Creates a new medical center request. Redirect endpoint from medical-centers/id POST ",
        manual_parameters=[
            openapi.Parameter(
                'medcent_id',
                openapi.IN_PATH,
                description="ID of the medical center request",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body= openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'speciality': openapi.Schema(type=openapi.TYPE_INTEGER, description='Speciality ID'),
                'procedure': openapi.Schema(type=openapi.TYPE_INTEGER, description='Procedure ID'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Name'),
                'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Patinet Surname'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Gender'),
                'birthday': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Birthday'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Phone Number'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Email'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='Patient Country Code'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='Patient City Name'),
                'disease_history': openapi.Schema(type=openapi.TYPE_STRING, description='Patient disease history as a text'),
                'previous_disease': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous disease as a text'),
                'previous_surgery': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous surgery as a text'),
                'previous_treatment': openapi.Schema(type=openapi.TYPE_STRING, description='Patient previous treatment as a text'),
                'other_comments': openapi.Schema(type=openapi.TYPE_STRING, description="Patient' other comments as a text"),
            },
            required=["__all__"],
            example={
                "speciality"      : 62,
                "procedure"       : 43,
                "name"            : "John",
                "surname"         : "Doe",
                "gender"        : "m",
                "birthday"      : "2000-2-7",
                "phone"         : "+901234567890",
                "email"         : "example@gmail.com",
                "country"       : "TR",
                "city"          : "Samsun",
                "disease_history"     : "Started on five months ago.",
                "previous_disease"    : "-",
                "previous_surgery"    : "-",
                "previous_treatment"  : "-",
                "other_comments"      : "-"
            }
        ),
        responses={
            200: openapi.Response(
                description="Medical Center request is successfully created.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Success message."
                        ),
                    },
                    example={
                        "message": "Medical Center request is successfully created.",
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
                        "detail": "Request data is invaild."
                    }
                )
            ),
            401: openapi.Response(
                description="Authentication failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing."
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
    # this endpoint is redirected from medical-centers/id POST
    # medical center id is already provided in urls so no need to in requests body
    def post(self, request, medcent_id):

        token       = request.COOKIES.get("jwt")
        payload     = isTokenValid(token=token)
        user, patient = getPatientByID(payload=payload)

        # get request data
        data = request.data
        # apply patient and medical center ID to data
        data['patient'] = patient.id 
        data['medical_center'] = medcent_id
        # fix city and country data
        city_object = City.objects.filter(name=data["city"]).first()
        country_object = Country.objects.filter(code2=data["country"]).first() 
        data["city"] = city_object.id
        data["country"] = country_object.id
        # serialize the data
        serializer = MedicalCenterRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "message": "Medical Center request is successfully created.",
                },
                status=status.HTTP_200_OK
            )   
            return response
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)