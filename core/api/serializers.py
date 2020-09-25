from rest_framework import serializers
from core.models import Item, OrderItem, Order
# from django_countries.serializers import CountryFieldMixin
# from django_countries.serializer_fields import CountryField


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'title',
            'price',
            'discount_price',
            'category',
            'label',
            'slug',
            'description',
        ]


# We need to get rid of Slug or id fields from create serializer

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'title',
            'price',
            'discount_price',
            'category',
            'label',
            'description',
        ]


class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()

