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


def get_dish_type(info):

    try:
        dish_type = DishType.objects.get(name=info['dish_type']['name'].lower())

    except DishType.DoesNotExist:
        dish_type = DishType.objects.create(name=info['dish_type']['name'].lower())
        dish_type.save()

    return dish_type


def get_dish_temperature(info):

    try:
        dish_temperature = DishTemperature.objects.get(name=info['dish_temperature']['name'].lower())

    except DishTemperature.DoesNotExist:
        dish_temperature = DishTemperature.objects.create(name=info['dish_temperature']['name'].lower())
        dish_temperature.save()

    return dish_temperature


def set_dish(info, dish_type, dish_temperature):

    try:
        dish = Dish.objects.get(name=info['name'])

    except Dish.DoesNotExist:
        dish = Dish.objects.create(name=info['name'], description=info['description'],
                                   dish_type=dish_type, dish_temperature=dish_temperature)

    return dish


def set_dish_available(dish, available):

    try:
        dish_available = DishAvailable.objects.get(dish=dish, temporary=available['temporary'],
                                              release_date=available['release_date'])

    except DishAvailable.DoesNotExist:
        dish_available = DishAvailable.objects.create(dish=dish, temporary=available['temporary'],
                                                      release_date=available['release_date'],
                                                      end_date=available['end_date'],
                                                      )

    return available


def set_ingredients(ingredient, dish):

    try:
        ing = Ingredient.objects.get(name=ingredient['ingredient']['name'])

    except Ingredient.DoesNotExist:
        ing = Ingredient.objects.create(name=ingredient['ingredient']['name'])

    try:
        DishIngredients.objects.get(dish=dish, ingredient=ing)

    except DishIngredients.DoesNotExist:
        DishIngredients.objects.create(dish=dish, ingredient=ing)


def set_steps(step, dish):

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


def get_orders_from(date_init, date_end, request):

    total = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end)
    n_total = len(total)
    total_data = OrderSerializer(total, many=True, context={'request': request}).data
    open = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end, finish=False, cancel=False)
    n_open = len(open)
    open_data = OrderSerializer(open, many=True, context={'request': request}).data
    correct = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end, finish=True)
    n_correct = len(correct)
    correct_data = OrderSerializer(correct, many=True, context={'request': request}).data
    canceled = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end, cancel=True)
    n_canceled = len(canceled)
    canceled_data = OrderSerializer(canceled, many=True, context={'request': request}).data
    response = {
        'resumen': {
            'total': n_total,
            'open': n_open,
            'finish': n_correct,
            'cancel': n_canceled
        },
        'total': total_data,
        'open': open_data,
        'finish': correct_data,
        'cancel': canceled_data

    }

    return response


def get_dishes_by_types(date_init, date_end, request):

    dishes = Dish.objects.all()
    total = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end).values_list('id', flat=True)
    canceled = Order.objects.filter(order_time__gte=date_init, order_time__lte=date_end, cancel=True).values_list('id', flat=True)
    response = {

        'total': total,
        'cancel': canceled

    }

    for i in dishes:
        response[i.name] = {}
        response[i.name]['total'] = len(OrderDishes.objects.filter(order__in=total, dish=i))
        response[i.name]['cancel'] = len(OrderDishes.objects.filter(order__in=canceled, dish=i))

    return response
