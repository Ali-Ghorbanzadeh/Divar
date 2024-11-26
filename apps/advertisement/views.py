from .serializer import CategorySerializer, ListAdSerializer, CreateUpdateRetrieveDeleteAdSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from .models import Category, Ad, Image
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


@method_decorator(cache_page(30), name='get')
class CategoryAPIView(ListAPIView, RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'title'

    def get(self, request, *args, **kwargs):
        if kwargs.get('title'):
            return super().retrieve(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)


@method_decorator(cache_page(30), name='get')
class ListAdAPIView(GenericAPIView):
    queryset = Ad.objects.all()
    serializer_class = ListAdSerializer

    def get(self, request, *args, **kwargs):
        if title := kwargs.get('title'):
            all_objects = Ad.get_ads(title)

        else:
            all_objects = Ad.get_ads()

        serializers = self.get_serializer(all_objects, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CreateUpdateDeleteRetrieveAdAPIView(RetrieveAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ad.objects.all()
    serializer_class = CreateUpdateRetrieveDeleteAdSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'سیستم درحال ثبت آگهی میباشد. لطفا صبور باشید'}, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({'message': 'درخواست نامعتبر!'},status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        advertisement = get_object_or_404(Ad, pk=request.data.get('pk'))
        serializer = self.get_serializer(advertisement, data=request.data, partial=True, context={'request': request})

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.save(force_update='updated_at')
        super().perform_destroy(instance)


