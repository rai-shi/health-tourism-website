from django.urls import path
from .views import * 

# ! medical center profile deletion 
urlpatterns = [
    # GET, PUT, PATCH
    path('profile/', MedicalCenterView.as_view(), name="profile"),  

    # GET, POST, DELETE  
    path('profile/doctors/', MedicalCenterDoctorsView.as_view(), name="doctors"),
    # GET, DELETE, PATCH
    path('profile/doctors/<int:id>/', MedicalCenterDoctorView.as_view(), name="doctor-detail"),
    
    # GET, PUT, DELETE
    path('profile/specialities/', MedicalCenterSpecialitiesView.as_view(), name="medcent-specialities"),                  
    path('profile/specialities/<int:speciality_id>', MedicalCenterSpecialitiesView.as_view(), name="medcent-speciality"), 
    # GET, DELETE
    path('profile/specialities/<int:speciality_id>/<int:procedure_id>', MedicalCenterProceduresView.as_view(), name="medcent-procedure"), 

    # GET, PUT, DELETE                 
    path('profile/insurances/', MedicalCenterHealthInsurancesView.as_view(), name="insurances"),
    # DELETE                
    # path('profile/insurances/<int:id>', MedicalCenterHealthInsuranceView.as_view(), name="insurance"),                  

    # GET, POST, DELETE
    path('profile/videos/', MedicalCenterVideosView.as_view(), name="videos"),         
    path('profile/videos/<int:id>', MedicalCenterVideosView.as_view(), name="video"),    

    # GET, POST, DELETE
    path('profile/photos/', MedicalCenterPhotosView.as_view(), name="videos"),         
    path('profile/photos/<int:id>', MedicalCenterPhotosView.as_view(), name="video"),         
     
    path('requests/', MedicalCenterRequestsView.as_view(), name="requests"),
    path('requests/filter/', FilteredMedicalCenterRequestsView.as_view(), name="filtered-requests")
  
    # path('medical-center-statistics/'),     # GET
]   