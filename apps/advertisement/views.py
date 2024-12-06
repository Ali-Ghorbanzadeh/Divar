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
from rest_framework.pagination import LimitOffsetPagination

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
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        category_title = kwargs.get('title')
        city = kwargs.get('city')
        if category_title and city:
            all_objects = Ad.get_ads(category__title=category_title, address__name=city)

        elif category_title:
            all_objects = Ad.get_ads(category__title=category_title)

        elif city:
            all_objects = Ad.get_ads(address__name=city)

        else:
            all_objects = Ad.get_ads()

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(all_objects, request)

        serializers = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializers.data)


class CreateUpdateDeleteRetrieveAdAPIView(RetrieveAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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

        except AssertionError as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        advertisement = get_object_or_404(Ad, pk=request.data.get('pk'))
        serializer = self.get_serializer(advertisement, data=request.data, partial=True, context={'request': request})

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response({'message': 'درخواست نامعتبر!'}, status=status.HTTP_400_BAD_REQUEST)

        except AssertionError as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.save(force_update='updated_at')
        super().perform_destroy(instance)


class SearchAdAPIView(GenericAPIView):
    queryset = Ad.objects.all()
    serializer_class = ListAdSerializer
    pagination_class = LimitOffsetPagination

    def post(self, request, *args, **kwargs):
        text = kwargs.get('text')
        category_title = request.data.get('category_title')
        city = request.data.get('city')
        order_by = request.data.get('order_by', '-created_at')

        if category_title and city:
            all_objects = Ad.get_ads(category__title=category_title, address__name=city, title__regex=text, order_by=order_by)

        elif category_title:
            all_objects = Ad.get_ads(category__title=category_title, title__regex=text, order_by=order_by)

        elif city:
            all_objects = Ad.get_ads(address__name=city, title__regex=text, order_by=order_by)

        else:
            all_objects = Ad.get_ads(title__regex=text, order_by=order_by)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(all_objects, request)

        serializers = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializers.data)

