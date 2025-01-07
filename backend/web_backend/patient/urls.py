from django.urls import path
from . import views 

urlpatterns = [
    path("login", views.Login, name="login"),
    path("register", views.Register, name="register"),
    path("logout", views.Logout, name="logout"),
    path("me", views.GetUserByID, name="me"),
    path("change-password", views.ChangePassword, name="change-password"),
    path("update-user-info", views.UpdateUserInfo, name="update-user-info"),
]   