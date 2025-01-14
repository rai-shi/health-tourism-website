from django.urls import path
from .views import * 

# ! medical center profile deletion 
urlpatterns = [
    # GET, PUT, PATCH
    path('profile/', MedicalCenterView.as_view(), name="profile"),  

    # POST, PUT, DELETE  
    path('doctors/', MedicalCenterDoctorsView.as_view(), name="update-information"),
    
    # path('medical-center-photos/'),         # POST, DELETE
    # path('medical-center-videos/'),         # POST, DELETE    
   
    # path('specialities/'),                  # POST, DELETE
    # path('procedure/'),                     # POST, DELETE
    # path('medical-center-photos/'),         # POST, DELETE
    # path('medical-center-videos/'),         # POST, DELETE
    # path('doctors/'),                       # POST, PUT, DELETE

    # path('medical-center-statistics/'),     # GET

]   