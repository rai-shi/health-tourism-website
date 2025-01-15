from django.urls import path
from .views import * 

# ! medical center profile deletion 
urlpatterns = [
    # GET, PUT, PATCH
    path('profile/', MedicalCenterView.as_view(), name="profile"),  

    # GET, POST, PATCH, DELETE  
    path('profile/doctors/', MedicalCenterDoctorsView.as_view(), name="doctors"),
    # GET, DELETE, PATCH
    path('profile/doctors/<int:pk>/', MedicalCenterDoctorsView.as_view(), name="doctor-detail"),
    
    # GET, PUT, DELETE
    path('profile/specialities/', MedicalCenterSpecialitiesView.as_view(), name="specialities"),                  
    path('profile/specialities/<int:pk>', MedicalCenterSpecialityView.as_view(), name="speciality"),                  
    
    # DELETE
    # path('profileprocedure/'),                    
    # path('profileprocedure/'),                    

    # path('medical-center-photos/'),         # POST, DELETE
    # path('medical-center-videos/'),         # POST, DELETE    
   


    # path('medical-center-statistics/'),     # GET

]   