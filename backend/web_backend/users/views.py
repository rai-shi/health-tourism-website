from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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
    # access token generation
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
        raise AuthenticationFailed("User not found!")
    return user

def checkPassword(user, password):
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password!")

def isTokenValid(token):
    if not token:
        raise AuthenticationFailed("Unauthenticated!")
    try:
        payload = jwt.decode(token, env("JWT_SECRET"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")
    return payload

def getUserByID(payload):
    user = User.objects.filter(id=payload["id"]).first()
    if not user:
        raise AuthenticationFailed("User not found!")
    return user



class RegisterView(APIView):
    def post(self, request):
        # get the data serialized as a json with UserSerializer using with User model.
        serializer = UserSerializers(data = request.data)
        # if data is valid
        serializer.is_valid(raise_exception=True)
        # then save the data to db or raise exception
        user = serializer.save()

        user_type = request.data.get("user_type", None)  # "patient" or "hospital"
        
        # create with default value
        if user_type == "patient":
            try:
                Patient.objects.create(user=user)
            except:
                # ! oluşturulan user'ı silmek gerekir
                return Response( 
                    {"message": "Patient registeration couldn't be done"}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
        elif user_type == "medical-center":
            try:
                MedicalCenter.objects.create(user=user)
            except:
                # ! oluşturulan user'ı silmek gerekir
                return Response( 
                    {"message": "Medical Center registeration couldn't be done"}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError({"user_type": "You must specify a valid user type ('patient' or 'medical-center')."})

        # return saved register data
        return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)

    
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User login",
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
                examples={
                    'application/json': {
                        'jwt': 'your_jwt_token_here'
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    'application/json': {
                        'detail': 'Invalid credentials'
                    }
                }
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
        
        # JWT configuration
        token = generateToken(user= user)
        response = Response()
        # cookie set backend only
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }
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

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data= {
            "message": "successfully logout"
        }
        return response
    
# ! email gönderimi ekle
class ChangePasswordView(APIView):
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
            raise AuthenticationFailed("Old password is incorrect!")
        # Check if the new password pair is matching
        if new_password1 != new_password2:
            raise ValidationError("The new passwords do not match.")

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
            raise AuthenticationFailed("Password is incorrect!")

        # Validate new email format
        try:
            email_validator = EmailValidator()
            email_validator(new_email)  # This will raise a ValidationError if email is invalid
        except DjangoValidationError:
            raise ValidationError("The new email address is not valid.")

        # Check if the new email is already taken
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email is already in use.")

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

