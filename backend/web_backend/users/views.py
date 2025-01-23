from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout, authenticate

# swagger documentation libs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError

import jwt, datetime, json, environ, os

from .serializers import UserSerializers
from .models import User
from patient.models import Patient
from medical_centers.models import MedicalCenter
from medical_centers.models import Speciality, Procedure, HealthInstitutions
from medical_centers.models import Doctor
from medical_centers.models import MedicalCenterPhotos, MedicalCenterVideos

from django.shortcuts import redirect
from django.urls import reverse
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))


def generateToken(user):
    # jwt access token generation
    payload = {
        "id": user.id,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.now()
    }
    # os.environ.get('JWT_SECRET')
    token = jwt.encode(payload, env("JWT_SECRET"), algorithm="HS256")
    return token

def getUserByEmail(email):
    user = User.objects.filter(email=email).first()
    if user is None:
        # raise AuthenticationFailed("User not found!")
        return Response(
            {"detail": "User not found!"},
            status= status.HTTP_404_NOT_FOUND
        )
    return user

def checkPassword(user, password):
    if not user.check_password(password):
        # raise AuthenticationFailed("Incorrect password!")
        return Response(
            {"detail": "Incorrect password!"},
            status= status.HTTP_401_UNAUTHORIZED
        )

def isTokenValid(token):
    if not token:
        # raise AuthenticationFailed("Unauthenticated!")
        return Response(
            {"detail": "Authentication token is missing."},
            status= status.HTTP_401_UNAUTHORIZED
        )
    try:
        payload = jwt.decode(token, env("JWT_SECRET"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # raise AuthenticationFailed("Unauthenticated!")
        return Response(
            {"detail": "Invalid or expired token."},
            status= status.HTTP_401_UNAUTHORIZED
        )
    return payload

def getUserByID(payload):
    user = User.objects.filter(id=payload["id"]).first()
    if not user:
        # raise AuthenticationFailed("User not found!")
        return Response(
                {"detail": "User not found!"},
                status= status.HTTP_404_NOT_FOUND
            )
    return user


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="User Register Endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User Last Name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User Password'),
                'user_type': openapi.Schema(type=openapi.TYPE_STRING, description='User Type (patient or medical-center)'),
            },
            example={
                'first_name': "John",
                'last_name': "Doe",
                'email': "example@gmail.com",
                'password': "your_password",
                'user_type': "patient or medical-center"
            },
            required=['first_name', 'last_name', 'email', 'password', 'user_type']
        ),
        responses={
            201: openapi.Response(
                description="Registeration successful.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='succesful message')
                    },
                    example={
                        "message" : "User succesfuly created." 
                    }
                )
            ),
            400: openapi.Response(
                description="Registration failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Registration failed: {error details}"
                    }
                )
            ),
             403: openapi.Response(
                description="validation error.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "You must specify a valid user type ('patient' or 'medical-center')."
                    }
                )
            )
        }
    )

    def post(self, request):
        # get the data serialized as a json with UserSerializer using with User model.
        serializer = UserSerializers(data = request.data)
        # if data is valid
        serializer.is_valid(raise_exception=True)
        # then save the data to db or raise exception
        user = serializer.save()

        user_type = request.data.get("user_type", None)  # "patient" or "hospital"
        
        # creation with default value
        # users can update their personal info in their profile
        try:
            if user_type == "patient":
                Patient.objects.create(user=user)
            elif user_type == "medical-center":
                MedicalCenter.objects.create(user=user)
            else:
                # raise ValidationError({"user_type": "You must specify a valid user type ('patient' or 'medical-center')."})
                return Response(
                   {"detail": "You must specify a valid user type ('patient' or 'medical-center')."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Exception as e:
            # if any error occurs and creation is failed then user also need to be deleted
            user.delete()  
            return Response(
                {"detail": f"Registration failed: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # return saved register data
        return Response(
                    {
                        "message" : "User succesfuly created." 
                    },
                    status=status.HTTP_201_CREATED
                    )

    
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User Login Endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful, JWT returned",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'jwt': openapi.Schema(type=openapi.TYPE_STRING, description='JWT token')
                    },
                    example={
                        'jwt': 'your_jwt_token_here'
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
                        'detail': 'User not found!'
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
                        'detail': 'Incorrect password.'
                    }
                )
            )
        }
    )

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        # find user by email
        user = getUserByEmail(email=email)
        # verify password
        checkPassword(user=user, password=password)

        # authenticate and login with django auth
        django_user = authenticate(request=request, email=email, password=password)
        login(request=request, user=django_user)

        # JWT configuration
        token = generateToken(user= user)
        response = Response()
        # cookie set backend only
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response

class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="User Logout Endpoint",
        responses={
            200: openapi.Response(
                description="Logout successful, JWT deleted",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Successfully Logout')
                    },
                    example={
                        'message': 'Successfully logout.'
                    }
                )
            )
        }
    )
    
    def post(self, request):
        response = Response()
        # delete token from cookies
        response.delete_cookie("jwt")
        response.data= {
            "message": "Successfully logout."
        }
        response.status_code = status.HTTP_200_OK
        # logout with django auth
        logout(request=request)
        return response
    
# ! email gönderimi ekle
class ChangePasswordView(APIView):
    @swagger_auto_schema(
        operation_description="User Change Password Endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='User old password'),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING, description='User new password'),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING, description='User new password for validation')
            },
            required=['old_password', 'new_password1', 'new_password2']
        ),
        responses={
            200: openapi.Response(
                description="Successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Successful message')
                    },
                    example={
                        "message": "Password successfully changed."
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "New passwords do not match."
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
                        "detail": "Authentication token is missing.",
                        "detail": "Invalid or expired token."
                    }
                )
            ),
            403: openapi.Response(
                description="Validation error.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Old password validation failed."
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
                        "detail": "User not found!"
                    }
                )
            ),
        }
    )

    def post(self, request):

        token = request.COOKIES.get("jwt")
        payload = isTokenValid(token=token)
        # Get the current user
        user = getUserByID(payload=payload)

        # Get the old and new passwords from the request data
        old_password = request.data.get("old_password")
        new_password1 = request.data.get("new_password1")
        new_password2 = request.data.get("new_password2")

        # Check if the old password matches
        if not user.check_password(old_password):
            # raise AuthenticationFailed("Old password is incorrect!")
            return Response(
                {"detail": "Old password validation failed."},
                status= status.HTTP_403_FORBIDDEN
            )
        
        # Check if the new password pair is matching
        if new_password1 != new_password2:
            # raise ValidationError("The new passwords do not match.")
            return Response(
                {"detail": "The new passwords do not match."},
                status= status.HTTP_400_BAD_REQUEST
            )

        # Serialize the data with the new password
        data = {
            "password": new_password1
        }
        serializer = UserSerializers(user, data=data, partial=True)

        # Validate and save the data 
        if serializer.is_valid():
            user.set_password(new_password1)
            user.save()

            response = Response(
                {"message": "Password successfully changed."},
                status=status.HTTP_200_OK
            )
            response.delete_cookie("jwt")  # Logout
            return response
        # validation error
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# ! send validation email
class UpdateEmailView(APIView):
    @swagger_auto_schema(
        operation_description="User Update Email Endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'new_email': openapi.Schema(type=openapi.TYPE_STRING, description='User new email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            },
            required=['new_email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful, JWT returned",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Successful message'),
                        'new_email': openapi.Schema(type=openapi.TYPE_STRING, description='New Email'),
                        'jwt': openapi.Schema(type=openapi.TYPE_STRING, description='JWT token')
                    },
                    example={
                        "message": "Email successfully changed.",
                        "new_email": 'your_new_email_here',
                        'jwt': 'your_jwt_token_here'
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Authentication token is missing.",
                        "detail": "Invalid or expired token."
                    }
                )
            ),
            403: openapi.Response(
                description="Validation error.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "Old password validation failed.",
                        "detail": "The new email address is not valid.",
                        "detail": "This email is already in use.",
                    }
                )
            ),
            404: openapi.Response(
                description="Unauthorized!",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details')
                    },
                    example={
                        "detail": "User not found!",
                    }
                )
            )
        }
    )

    def post(self, request):
        token = request.COOKIES.get("jwt")
        
        payload = isTokenValid(token=token)

        # Get the current user
        user =getUserByID(payload=payload)

        # Get the old password and new email from the request data
        password = request.data.get("password")
        new_email = request.data.get("new_email")

        # Check if the old password matches
        if not user.check_password(password):
            # raise AuthenticationFailed("Password is incorrect!")
            return Response(
                {"detail": "Old password validation failed."},
                status= status.HTTP_403_FORBIDDEN
            )
        # Validate new email format
        try:
            email_validator = EmailValidator()
            email_validator(new_email)  # This will raise a ValidationError if email is invalid
        except DjangoValidationError:
            # raise ValidationError("The new email address is not valid.")
            return Response(
                {"detail": "The new email address is not valid."},
                status= status.HTTP_403_FORBIDDEN
            )

        # Check if the new email is already taken
        if User.objects.filter(email=new_email).exists():
            # raise ValidationError("This email is already in use.")
            return Response(
                {"detail": "This email is already in use."},
                status= status.HTTP_403_FORBIDDEN
            )

        # Update the email
        user.email = new_email
        user.save()

        new_token = generateToken(user=user)

        # Send a response with the new JWT token and a success message
        response = Response(
            {
                "message": "Email successfully changed.",
                "new_email": new_email,
                "jwt": new_token  # Send the new token in the response
            },
            status=status.HTTP_200_OK
        )

        # Delete the old JWT token (we've already generated a new one)
        response.delete_cookie("jwt")

        # Set the new token in a secure, httpOnly cookie, 
        # set the new token only for backend
        response.set_cookie(key="jwt", value=new_token, httponly=True)

        return response





# /me -> gerek yok patient/me hospital/me den ulaşılacak
# class UserView(APIView):
#     def get(self, request):
#         token = request.COOKIES.get("jwt")
#         payload = isTokenValid(token=token)
#         user = getUserByID(payload)

#         # make the response data json valid
#         serializer = UserSerializers(user)
#         return Response(serializer.data)