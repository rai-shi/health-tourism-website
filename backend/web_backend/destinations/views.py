from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.views import *
from .models import *
from .serializers import *

from django.shortcuts import redirect
from django.urls import reverse

class Destinations(APIView):
    def get(self, request, id=None):
        # no need to login

        if id is not None:
            try: 
                destination = Destination.objects.get(id=id)
            except:
                return Response(
                    {"message": "Destination is not found!"},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = DestinationSerializer(destination)

            response = Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
            return response
        
        # else
        try: 
            destinations = Destination.objects.all()
        except:
            return Response(
                {"message": "Not found any destination record!"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = DestinationListSerializer(destinations, many= True)

        response = Response(
            serializer.data,
            status= status.HTTP_200_OK
        )
        return response