from django.urls import path
from .views import * 

urlpatterns = [

    path("me", 
        PatientView.as_view(), 
        name="me"),

    path("update-personal-info", 
        UpdatePersonalInfoView.as_view(), 
        name="update-personal-info"),

    path("medical-center-request", 
        RequestToMedicalCenterView.as_view(), 
        name="medical-center-request")
    
]   