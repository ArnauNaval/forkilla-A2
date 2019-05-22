from .models import Restaurant, Review
from rest_framework import serializers
from django.contrib.auth.models import User


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'restaurant_number', 'name', 'menu_description',
            'price_average', 'is_promot', 'rate', 'address',
            'city', 'country', 'featured_photo', 'category',
            'capacity'
        )

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    class Meta:
        model = Review
        fields = ('id', 'restaurant','message', 'rate', 'user')


