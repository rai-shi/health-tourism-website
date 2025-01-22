from django.urls import path
from .views import * 

urlpatterns = [

    path("me", 
        PatientView.as_view(), 
        name="me"),

    path("update-personal-info/", 
        UpdatePersonalInfoView.as_view(), 
        name="update-personal-info"),

    path("requests/", 
        RequestsView.as_view(), 
        name="requests"),

    path("requests/<int:id>", 
        RequestView.as_view(), 
        name="request"),

    path("medical-center-request/<int:medcent_id>/", 
        RequestToMedicalCenterView.as_view(), 
        name="medical-center-request")
    
]   