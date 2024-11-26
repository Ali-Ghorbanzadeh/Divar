from django.urls import path
from .views import CategoryAPIView, ListAdAPIView, CreateUpdateDeleteRetrieveAdAPIView

urlpatterns = [
    path('api/category/', CategoryAPIView.as_view(), name='category'),
    path('api/category/<str:title>/', CategoryAPIView.as_view(), name='category-id'),
    path('api/advertisement/create/', CreateUpdateDeleteRetrieveAdAPIView.as_view(), name='advertisement'),
    path('api/advertisement/update/', CreateUpdateDeleteRetrieveAdAPIView.as_view(), name='advertisement'),
    path('api/advertisement/delete/<int:pk>/', CreateUpdateDeleteRetrieveAdAPIView.as_view(), name='advertisement'),
    path('api/advertisement/<int:pk>/', CreateUpdateDeleteRetrieveAdAPIView.as_view(), name='show-advertisement'),
    path('api/home/advertisement/', ListAdAPIView.as_view(), name='show-all-advertisements'),
    path('api/advertisement/<str:title>/', ListAdAPIView.as_view(), name='show-advertisement-by-category')
]
