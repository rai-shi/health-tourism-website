from django.urls import path
from .views import * 

urlpatterns = [
    path("", AdminView.as_view(), name="landing-page"),
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", AdminLogoutView.as_view(), name="logout"),

    path("users/", AdminUsersView.as_view(), name="users-list"),
    path("users/create/", AdminUserCreateView.as_view(), name="user-create"),

    path("specialities/", AdminSpecialitiesView.as_view(), name="specialities"),

    path("procedures/", AdminProceduresView.as_view(), name="procedures"),

    path("insurances/", AdminInsurancesView.as_view(), name="insurances"),

    path("destinations/", AdminDestinationsView.as_view(), name="destinations"),

    path("requests/", AdminRequestsView.as_view(), name="requests"),

    path("blogs/", AdminBlogView.as_view(), name="blog"),

    path("aboutus/", AdminView.as_view(), name="aboutus"),


]

