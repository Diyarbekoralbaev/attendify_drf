from django.urls import path
from .views import RegisterView, LoginView, MeView, UserDetailView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
