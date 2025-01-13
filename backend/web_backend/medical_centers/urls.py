from django.urls import path
from .views import * 

urlpatterns = [
    path('profile/', MedicalCenterView.as_view(), name="profile"),                          # GET
    # path('medical-center-statistics/'),     # GET
    path('update-information/', UpdateMedicalCenterInfoView.as_view(), name="update-information"),    # PUT
    # path('preview-text'),                   # PUT, DELETE
    # path('overview-text'),                  # PUT, DELETE
    # path('specialities/'),                  # POST, DELETE
    # path('procedure/'),                     # POST, DELETE
    # path('medical-center-photos/'),         # POST, DELETE
    # path('medical-center-videos/'),         # POST, DELETE
    # path('doctors/'),                       # POST, PUT, DELETE

]   