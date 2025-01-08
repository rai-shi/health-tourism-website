from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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

def ChangePassword(request):
    pass 

def UpdateEmail(request):
    pass 




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