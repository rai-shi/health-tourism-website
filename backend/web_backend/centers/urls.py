from django.urls import path
from .views import * 

urlpatterns = [

    path('', MedicalCentersView.as_view(), name="med-centers"),  
    path('<int:id>/', MedicalCentersView.as_view(), name="med-center"),  
]   