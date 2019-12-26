from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DishTypeViewSet(viewsets.ModelViewSet):
    queryset = DishType.objects.all()
    serializer_class = DishTypeSerializer


class DishTemperatureViewSet(viewsets.ModelViewSet):
    queryset = DishTemperature.objects.all()
    serializer_class = DishTemperatureSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TimeUnitsViewSet(viewsets.ModelViewSet):
    queryset = TimeUnits.objects.all()
    serializer_class = TimeUnitsSerializer


class DishIngredientsViewSet(viewsets.ModelViewSet):
    queryset = DishIngredients.objects.all()
    serializer_class = DishIngredientsSerializer


class DishStepsViewSet(viewsets.ModelViewSet):
    queryset = DishSteps.objects.all()
    serializer_class = DishStepsSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishAvailableViewSet(viewsets.ModelViewSet):
    queryset = DishAvailable.objects.all()
    serializer_class = DishAvailableSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTrackViewSet(viewsets.ModelViewSet):
    queryset = OrderTrack.objects.all()
    serializer_class = OrderTrackSerializer


class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer


class OrderDishesViewSet(viewsets.ModelViewSet):
    queryset = OrderDishes.objects.all()
    serializer_class = OrderDishesSerializer


class ClientDishViewSet(viewsets.ModelViewSet):
    queryset = ClientDish.objects.all()
    serializer_class = ClientDishSerializer


import json
@api_view(['POST'])
def add_new_dish(request):
    print(type(request.data))
    #print(type(request.data['people'][0]))
    json_string = json.dumps(request.data)
    datastore = json.loads(json_string)
    print(type(datastore))
    print(datastore['eBooks'])
    #js = json.loads(request.data[0])
    return Response(datastore)


def send_email(send_to, subject, email_from, text=None, obj=None, type=None):

    print(send_to)
    print(subject)
    print(email_from)
    print(text)
    return text


def persons_send_activation_email(pk):
    try:
        #person = Client.objects.get(pk=pk)

        subject = 'Activación usuario'
        email_from = 'asd@mailACambiar.com'
        send_to = ''
        url = 'API/utilities/components/user_email_activation_template.html'
        tipo = 'activation_mail'
        response = send_email(send_to, subject, email_from, type=tipo)

        return response

    except Client.DoesNotExist:
        raise Http404


import requests
@api_view(['GET'])
def add_dish(request):

    try:
        json_string = json.dumps(request.data)
        datastore = json.loads(json_string)
        response = requests.get("http://localhost:8000/api/")

        return Response(response)

    except Client.DoesNotExist:
        raise Http404


@api_view(['POST'])
def post_dish(request):

    try:
        json_string = json.dumps(request.data)
        datastore = json.loads(json_string)
        for ingredient in datastore['ingredient']:
            requests.post("http://localhost:8000/api/ingredient/", json=ingredient)

        for step in datastore['steps']:
            requests.post("http://localhost:8000/api/dish_steps/", json=ingredient)

        return Response('Done')

    except Client.DoesNotExist:
        raise Http404


'''  
To Change
The system should provide API for the following features:
● Provide menu of the restaurant (different pizza recipes, side dishes, drinks)
● Place orders
● Track execution of an order
● Execute pizza cooking with regards to the order queue
● Provide statistical data about the restaurant
'''
@api_view(['GET'])
def get_menu(request):
    print("Return the menu")


@api_view(['GET'])
def dish_info(request):
    print('Dish details function')


@api_view(['POST'])
def new_order(request):
    print('New order')


@api_view(['GET'])
def track_order(request):
    print('Track order')


@api_view(['GET'])
def queue_time(request):
    print('Track order details')


@api_view(['GET'])
def statistics(request):
    print('Statistics')


@api_view(['GET'])
def recommendations(request):
    print('recommendations')
