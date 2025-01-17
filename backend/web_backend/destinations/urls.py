from django.urls import path
from .views import * 

urlpatterns = [

    path('', Destinations.as_view(), name="destinations"),  
    path('<int:id>', Destinations.as_view(), name="destination"),  
]   