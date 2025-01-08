from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError

import jwt, datetime, json, environ, os

from .serializers import UserSerializers
from .models import User

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))


class RegisterView(APIView):
    def post(self, request):
        # get the data serialized as a json with UserSerializer using with User model.
        serializer = UserSerializers(data = request.data)
        # if data is valid
        serializer.is_valid(raise_exception=True)
        # then save the data to db or raise exception
        serializer.save()
        # return saved register data
        return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        # find user by email
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found!")
        # verify password
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        # JWT configuration
        # access token generation
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }
        # os.environ.get('JWT_SECRET')
        token = jwt.encode(payload, env("JWT_SECRET"), algorithm="HS256")
        response = Response()
        # cookie set backend only
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response

# /me
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, env("JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializers(user)

        return Response(serializer.data)

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
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, env("JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the current user
        user = User.objects.filter(id=payload["id"]).first()
        if not user:
            raise AuthenticationFailed("User not found!")

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
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# ! send validation email

class ChangeEmailView(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, env("JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Get the current user
        user = User.objects.filter(id=payload["id"]).first()

        if not user:
            raise AuthenticationFailed("User not found!")

        # Get the old password and new email from the request data
        old_password = request.data.get("old_password")
        new_email = request.data.get("new_email")

        # Check if the old password matches
        if not user.check_password(old_password):
            raise AuthenticationFailed("Old password is incorrect!")

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

        # Generate new JWT token since email is changed
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }
        new_token = jwt.encode(payload, env("JWT_SECRET"), algorithm="HS256")

        # Send a response with the new JWT token and a success message
        response = Response(
            {
                "message": "Email successfully changed.",
                "new_email": new_email,
                "jwt": new_token  # Send the new token in the response
            },
            status=status.HTTP_200_OK
        )

        # Optional: Delete the old JWT token (we've already generated a new one)
        response.delete_cookie("jwt")

        # Set the new token in a secure, httpOnly cookie
        response.set_cookie(key="jwt", value=new_token, httponly=True)

        return response


# ! JWT Token kısmını fonksiyonlaştır
# {
#     "first_name": "ayse",
#     "last_name": "tak",
#     "email": "ayse4@gmail.com",
#     "password": "930615Fly"
# }

# {
#  "email": "ayse@gmail.com",
# "password": "930615Fly"
# }

# {
# "old_password" : "930615Fly",
# "new_password" : "591003Black"
# }