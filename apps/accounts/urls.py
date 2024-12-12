from django.urls import path
from .views import LoginAndVerifyAPIView, UserUpdateAPIView, LogoutView

urlpatterns = [
    path('api/login/', LoginAndVerifyAPIView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', UserUpdateAPIView.as_view(), name='profile')
]
