from django.urls import path
from .views import * 

urlpatterns = [

    path('', MedicalCentersView.as_view(), name="med-centers"),  
    path('<int:id>/', MedicalCentersByIDView.as_view(), name="med-center"),  

    path('<int:speciality_id>/<int:procedure_id>/', SpecialityBasedFilteredMedicalCentersView.as_view(), name="filtered-medcenters"),  
    
    path('filter/', FilteredMedicalCentersView.as_view(), name="filtered-medcenters"),  
    
    

]   

