from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class DishTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishType
        fields = '__all__'


class DishTemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishTemperature
        fields = '__all__'


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TimeUnitsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeUnits
        fields = '__all__'


class DishIngredientsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishIngredients
        fields = '__all__'


class DishIngredientsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishIngredients
        fields = ['ingredient']
        depth = 1


class DishStepsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishSteps
        fields = '__all__'


class DishStepsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishSteps
        exclude = ['dish']
        depth = 2


class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DishDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
        depth = 3


class DishAvailableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishAvailable
        fields = '__all__'


class DishAvailableDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishAvailable
        exclude = ['dish']


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderTrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderTrack
        fields = '__all__'


class ClientAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientAddress
        fields = '__all__'


class OrderDishesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDishes
        fields = '__all__'
