import datetime
from .models import *
from .serializers import *


def order_notification(instance):
    if instance.end:
        print("Dish "+instance.order.dish.name+" of order no "+str(instance.order.order.id)+
              " Update. Finished! Bon Appetit! ")
    else:
        print("Dish "+instance.order.dish.name+" of order no "+str(instance.order.order.id)+" Update. Step "
              + str(instance.step))


def get_user(client):
    print(type(client))
    print(client['identification_card'])
    return Client.objects.get(identification_card=client['identification_card'], mail=client['mail'])


def get_address(client, address):
    try:
        ca = ClientAddress.objects.get(client=client, address=address['address'], city=address['city'])

    except:
        ca = ClientAddress.objects.create(client=client, address=address['address'], city=address['city'],
                                          postal_code=address['postal_code'])
    return ca


def add_order(client, client_address):
    order_time = datetime.datetime.today()
    return Order.objects.create(client=client, client_address=client_address, order_time=order_time)


def add_dish(order, dish):
    d = Dish.objects.get(name=dish['name'])
    order_dish = OrderDishes.objects.create(dish=d, order=order)
    OrderTrack.objects.create(order=order_dish, step=1)
    return d


def order_track(order, dish):
    d = Dish.objects.get(name=dish['name'])
    OrderDishes.objects.create(dish=d, order=order)
    return d


def get_dish_track(dish, step):
    d = DishSteps.objects.filter(dish=dish, no_step__gte=step)
    return d


def get_dish_time(dish, step):
    d = DishSteps.objects.filter(dish=dish, no_step__gte=step)
    time = 0
    for steptime in d:
        mult = {
        1: 60,
        2: 1,
        3: 3600
        }
        time += (steptime.time*mult.get(steptime.time_units.id))
    return time


def order_data(order, request):
    dishes = OrderDishes.objects.filter(order=order)
    list_status = []
    for dish in dishes:
        plate = DishSerializer(dish.dish, context={'request': request}).data
        steps = DishStepsSerializer(DishSteps.objects.filter(dish=dish.dish.id),many=True,
                                    context={'request': request}).data
        status = OrderTrackSerializer(OrderTrack.objects.get(order=dish.id), context={'request': request}).data
        time_to = get_dish_time(dish.dish.id, status['step'])
        list_status.append({'dish': plate, 'status': status, 'steps': steps, 'time':time_to})

    return list_status


def time_order(order, request):
    queue = Order.objects.filter(pk__lt=order.id, finish=False, cancel=False)
    my_order = order_data(order, request)
    orders_queue = []
    time_previous = 0
    for i in queue:
        tmp = order_data(i, request)
        orders_queue.append(tmp)
        for j in tmp:
            time_previous += j['time']

    my_time = 0
    for q in my_order:
        my_time += q['time']

    total_time = time_previous + my_time

    return [time_previous, my_time, total_time, len(queue)]
    '''
    for odr in queue:
        command = OrderDishes.objects.filter(order=odr)
        for ()
        dish_command=


    dishes = OrderDishes.objects.filter(order=order)
    list_status = []
    for dish in dishes:
        plate = DishSerializer(dish.dish, context={'request': request}).data
        steps = DishStepsSerializer(DishSteps.objects.filter(dish=dish.dish.id),many=True,
                                    context={'request': request}).data
        status = OrderTrackSerializer(OrderTrack.objects.get(order=dish.id), context={'request': request}).data
        list_status.append({'dish': plate, 'status': status, 'steps': steps})

    return list_status
    '''