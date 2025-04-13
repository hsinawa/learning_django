from django.urls import path
from users.views import RegisterView, LoginView, VerifyEmailView,AddPermissions

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('verify-email', VerifyEmailView.as_view(), name='verify_email'),
    path('add-permission', AddPermissions.as_view(), name='add_permission'),
]
