from django.urls import path
from .views import AdPaymentsAPIView

urlpatterns = [
    path('api/payments/status/<int:pk>', AdPaymentsAPIView.as_view(), name='get-or-update-payments'),
    path('api/payments/create/', AdPaymentsAPIView.as_view(), name='create-payments')
]