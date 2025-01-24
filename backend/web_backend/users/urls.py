from django.urls import path
from .views import LoginView, RegisterView, LogoutView, ChangePasswordView, UpdateEmailView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),                               # POST
    path("register", RegisterView.as_view(), name="register"),                      # POST                             
    path("logout", LogoutView.as_view(), name="logout"),                            # POST
    path("change-password", ChangePasswordView.as_view(), name="change-password"),  # POST
    path("update-email", UpdateEmailView.as_view(), name="update-email"),           # POST

    # path("me", UserView.as_view(), name="me"),                                    # no need, each user role have own profile url
]

