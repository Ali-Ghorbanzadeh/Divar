from django.urls import path
from .views import LoginAndVerifyAPIView, UserUpdateAPIView, LogoutView, UserAdHistoryAPIView

urlpatterns = [
    path('api/login/', LoginAndVerifyAPIView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', UserUpdateAPIView.as_view(), name='profile'),
    path('api/profile/history/<int:pk>/', UserAdHistoryAPIView.as_view(), name='ads-history'),
]
