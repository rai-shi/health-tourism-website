from django.urls import path
from .views import * 

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("me", UserView.as_view(), name="me"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("change-password", ChangePassword, name="change-password"),
    path("update-email", UpdateEmail, name="update-email"),
]