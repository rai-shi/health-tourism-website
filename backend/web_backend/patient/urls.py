from django.urls import path
from . import views 

urlpatterns = [
    
    path("me", 
         views.GetPatientUserByID, 
         name="me"),
    path("medical-center-request", 
         views.RequestToMedicalCenter, 
         name="medical-center-request")
    
]   