from django.urls import path
from .views import * 

urlpatterns = [

    # GET, POST (for updating)
    path("me", 
        PatientView.as_view(), 
        name="me"),
    # GET, POST
    path("requests/", 
        RequestsView.as_view(), 
        name="requests"),
    # GET
    path("requests/<int:id>", 
        RequestView.as_view(), 
        name="request"),
    # POST
    path("medical-center-request/<int:medcent_id>/", 
        RequestToMedicalCenterView.as_view(), 
        name="medical-center-request")
    
]   


# path("update-personal-info/", 
#         UpdatePersonalInfoView.as_view(), 
#         name="update-personal-info"),