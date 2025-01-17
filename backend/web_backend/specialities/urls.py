from django.urls import path
from .views import * 

urlpatterns = [

    path('', SpecialitiesView.as_view(), name="specialities"),  
    
]   