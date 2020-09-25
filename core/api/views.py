from requests import Response
from rest_framework import generics, status
from core.models import Item, CountryField
from django_countries import Countries, countries

from .serializers import *


# This API is for Listing of objects and filtering it thorugh 'title' keyword parameter
class ItemListAPIView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = ItemSerializer

    def get_queryset(self):
        qs = Item.objects.all()
        query = self.request.GET.get('title')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


# We need to get rid of Slug or id fields from create serializer
class ItemCreateAPIView(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CountryListAPI(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = countries
    serializer_class = CountrySerializer
