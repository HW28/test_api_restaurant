import datetime
import requests
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .functions import *
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .serializers import *
from .models import *
from itertools import chain
import time


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


@api_view(['GET'])
def get_dish(request):

    try:
        dish = request.headers.get('dish')
        dish_info = Dish.objects.filter(pk=dish)
        dish_availability = DishAvailable.objects.filter(dish=dish)
        dish_ingredients = DishIngredients.objects.filter(dish=dish)
        dish_steps = DishSteps.objects.filter(dish=dish).order_by('no_step')
        dish_info_data = DishDetailSerializer(dish_info, many=True, context={'request': request}).data
        dish_availability_data = DishAvailableDetailSerializer(dish_availability, many=True,
                                                               context={'request': request}).data
        dish_ingredients_data = DishIngredientsDetailSerializer(dish_ingredients, many=True,
                                                                context={'request': request}).data
        dish_steps_data = DishStepsDetailSerializer(dish_steps, many=True, context={'request': request}).data
        response = {
            'info': dish_info_data,
            'available': dish_availability_data,
            'ingredients': dish_ingredients_data,
            'steps': dish_steps_data
        }

        return Response(response)

    except Dish.DoesNotExist:
        raise Http404


@api_view(['POST'])
def post_dish(request):

    try:

        json_string = json.dumps(request.data)
        datastore = json.loads(json_string)

        for info in datastore['info']:

            try:
                dish_type = DishType.objects.get(name=info['dish_type']['name'].lower())

            except DishType.DoesNotExist:
                dish_type = DishType.objects.create(name=info['dish_type']['name'].lower())
                dish_type.save()

            try:
                dish_temperature = DishTemperature.objects.get(name=info['dish_temperature']['name'].lower())

            except DishTemperature.DoesNotExist:
                dish_temperature = DishTemperature.objects.create(name=info['dish_temperature']['name'].lower())
                dish_temperature.save()

            try:
                dish = Dish.objects.get(name=info['name'])

            except Dish.DoesNotExist:
                dish = Dish.objects.create(name=info['name'], description=info['description'],
                                           dish_type=dish_type, dish_temperature=dish_temperature)

        for available in datastore['available']:

            try:
                DishAvailable.objects.get(dish=dish, temporary=available['temporary'],
                                          release_date=available['release_date'])

            except DishAvailable.DoesNotExist:
                DishAvailable.objects.create(dish=dish, temporary=available['temporary'],
                                             release_date=available['release_date'],
                                             end_date=available['end_date'],
                                             )

        for ingredient in datastore['ingredients']:

            try:
                ing = Ingredient.objects.get(name=ingredient['ingredient']['name'])

            except Ingredient.DoesNotExist:
                ing = Ingredient.objects.create(name=ingredient['ingredient']['name'])

            try:
                DishIngredients.objects.get(dish=dish, ingredient=ing)

            except DishIngredients.DoesNotExist:
                DishIngredients.objects.create(dish=dish, ingredient=ing)

        for step in datastore['steps']:

            try:
                time_unit = TimeUnits.objects.get(name=step['time_units']['name'])

            except TimeUnits.DoesNotExist:
                time_unit = TimeUnits.objects.create(name=step['time_units']['name'])

            try:
                DishSteps.objects.get(dish=dish, no_step=step['no_step'])

            except DishSteps.DoesNotExist:
                DishSteps.objects.create(dish=dish, no_step=step['no_step'], step=step['step'], time=step['time'],
                                         ingredients=step['ingredients'], time_units=time_unit
                                         )

        return Response('Done')

    except Client.DoesNotExist:
        raise Http404


@api_view(['GET'])
def get_menu(request):

    today = datetime.date.today()
    dish_availability = DishAvailable.objects.filter(temporary=False)
    dish_promotion = DishAvailable.objects.filter(temporary=True, release_date__lte=today, end_date__gte=today)
    result_list = list(chain(dish_availability, dish_promotion))
    dish_menu = []

    for available in result_list:
        dish_menu.append(available.dish.id)

    dish = Dish.objects.filter(pk__in=dish_menu)
    dish_data = DishSerializer(dish, many=True, context={'request': request}).data

    return Response(dish_data)


@api_view(['POST'])
def post_order(request):

    json_string = json.dumps(request.data)
    datastore = json.loads(json_string)
    client = get_user(datastore['client'])
    client_address = get_address(client, datastore['address'])
    order = add_order(client, client_address)
    dishes = []

    for dish in datastore['dish']:
        dishes.append(add_dish(order, dish))

    order_data = OrderSerializer(order, context={'request': request}).data
    client_data = ClientSerializer(client, context={'request': request}).data
    address_data = ClientAddressSerializer(client_address, context={'request': request}).data
    dish_data = DishSerializer(dishes, many=True, context={'request': request}).data
    response = {
        'no_order': order.id,
        'order': order_data,
        'client': client_data,
        'address': address_data,
        'dishes': dish_data
    }

    return Response(response)


@api_view(['GET'])
def get_open_orders(request):

    email = request.headers.get('email')
    identification_card = request.headers.get('id')
    client_temp = {"mail": email, "identification_card": identification_card}
    client = get_user(client_temp)
    orders = Order.objects.filter(client=client, finish=False)
    list_orders = []

    for order in orders:
        order_data = OrderSerializer(order, context={'request': request}).data
        list_orders.append({'no_order': order.id, 'order': order_data})

    response = list_orders

    return Response(response)


@api_view(['GET'])
def track_order(request):

    email = request.headers.get('email')
    identification_card = request.headers.get('id')
    order = request.headers.get('order')

    return Response(order_data(order, request))


@api_view(['GET'])
def queue_time(request):

    order = request.headers.get('order')
    queue_info = time_order(Order.objects.get(pk=order), request)
    response = {
        'queue': queue_info[3],
        'queue time': time.strftime('%H:%M:%S', time.gmtime(queue_info[0])),
        'order time': time.strftime('%H:%M:%S', time.gmtime(queue_info[1])),
        'total time': time.strftime('%H:%M:%S', time.gmtime(queue_info[2]))
    }

    return Response(response)


'''  
To Change
The system should provide API for the following features:
● Provide statistical data about the restaurant
'''


@api_view(['GET'])
def statistics(request):
    return Response('Statistics')


@api_view(['GET'])
def recommendations(request):
    return Response('recommendations')

