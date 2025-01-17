from django.urls import path
from .views import * 
from centers.views import FilteredMedicalCentersView

urlpatterns = [
    # GET 
    path('', SpecialitiesView.as_view(), name="specialities"),  
    path('<int:speciality_id>/<int:procedure_id>', SpecialityProcedureSelectionView.as_view(), name="filtered-medcenters"),  
    
    
]   