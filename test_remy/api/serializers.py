from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


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


class DishStepsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishSteps
        fields = '__all__'


class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DishAvailableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DishAvailable
        fields = '__all__'


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


class ClientDishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientDish
        fields = '__all__'
