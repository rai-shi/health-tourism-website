from django.urls import path
from .views import * 

urlpatterns = [
    path("", AdminView.as_view(), name="landing-page"),
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", AdminLogoutView.as_view(), name="logout"),
    path("users/", AdminUsersView.as_view(), name="users-list"),
    path("users/create/", AdminUsersView.as_view(), name="user-create"),
    path("specialities/", AdminView.as_view(), name="specialities"),
    path("procedures/", AdminView.as_view(), name="procedures"),
]

