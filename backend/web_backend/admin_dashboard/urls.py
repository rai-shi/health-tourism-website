from django.urls import path
from .views import * 

urlpatterns = [
    path("", AdminView.as_view(), name="landing-page"),

    # GET POST
    path("login/", AdminLoginView.as_view(), name="login"),
    # POST
    path("logout/", AdminLogoutView.as_view(), name="logout"),
    # GET 
    path("users/", AdminUsersView.as_view(), name="users-list"),

    path("users/create/", AdminUserCreateView.as_view(), name="user-create"),
    # GET, POST 
    path("specialities/", AdminSpecialitiesView.as_view(), name="specialities"),
    # POST, DELETE
    path("specialities/<int:id>", AdminSpecialitiesView.as_view(), name="specialities"),
    # DELETE
    path("specialities/<int:speciality_id>/<int:procedure_id>", AdminProceduresView.as_view(), name="procedures"),

    path("insurances/", AdminInsurancesView.as_view(), name="insurances"),
    path("insurances/<int:id>", AdminInsurancesView.as_view(), name="insurances"),

    path("destinations/", AdminDestinationsView.as_view(), name="destinations"),

    path("requests/", AdminRequestsView.as_view(), name="requests"),

    path("blogs/", AdminBlogView.as_view(), name="blog"),

    path("aboutus/", AdminView.as_view(), name="aboutus"),


]

