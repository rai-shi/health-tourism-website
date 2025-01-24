from django.urls import path
from .views import * 

urlpatterns = [

    # GET
    path('', MedicalCentersView.as_view(), name="med-centers"),  

    # GET, POST (for redirection)
    path('<int:id>/', MedicalCentersByIDView.as_view(), name="med-center"),  

    # GET
    path('<int:speciality_id>/<int:procedure_id>/', SpecialityBasedFilteredMedicalCentersView.as_view(), name="filtered-medcenters"),  
    
    # GET
    path('filter/', FilteredMedicalCentersView.as_view(), name="filtered-medcenters"),  
]   

