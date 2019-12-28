from django.db import models
from django.contrib.auth.models import User
import re


class DishType(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'dish_type'

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(DishType, self).save(*args, **kwargs)


class DishTemperature(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'dish_temperature'

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(DishTemperature, self).save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'ingredient'

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Ingredient, self).save(*args, **kwargs)


class TimeUnits(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'time_units'

    def __str__(self):
        return '%s' % self.name


class DishIngredients(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dish_ingredients'

    def __str__(self):
        return '%s' % self.ingredient


class DishSteps(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    no_step = models.IntegerField()
    step = models.TextField()
    time = models.IntegerField()
    time_units = models.ForeignKey('TimeUnits', on_delete=models.CASCADE)
    ingredients = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = 'dish_steps'

    def __str__(self):
        return '%s' % self.dish+' '+str(self.no_step)


class Dish(models.Model):
    name = models.CharField(max_length=50)
    dish_type = models.ForeignKey('DishType', on_delete=models.CASCADE)
    dish_temperature = models.ForeignKey('DishTemperature', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dish'

    def __str__(self):
        return '%s' % self.name


class DishAvailable(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    temporary = models.BooleanField(default=False)
    release_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'dish_available'

    def __str__(self):
        return '%s' % self.dish


class Client(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=25)
    identification_card = models.CharField(max_length=25, unique=True, blank=True, null=True)
    mail = models.EmailField()
    temporal = models.BooleanField(default=False)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return '%s' % self.name+' '+self.surname

    def save(self, *args, **kwargs):
        self.identification_card = self.identification_card.lower()
        self.identification_card = re.sub(r'[^a-z0-9]', r'', self.identification_card)
        super(Client, self).save(*args, **kwargs)


class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    client_address = models.ForeignKey('ClientAddress', on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    deliver_time = models.DateTimeField(blank=True, null=True)
    finish = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return '%s' % str(self.client)+' '+str(self.order_time)+' '+str(self.pk)

    def save(self, *args, **kwargs):
        if not self.cancel:
            self.cancel_reason = None
        super(Order, self).save(*args, **kwargs)


class ClientAddress(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=5)

    class Meta:
        db_table = 'client_address'

    def __str__(self):
        return '%s' % self.address+' '+self.city


class OrderDishes(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_dish'

    def __str__(self):
        return '%s' % self.order


class OrderTrack(models.Model):
    order = models.ForeignKey(OrderDishes, on_delete=models.CASCADE)
    step = models.IntegerField()
    end = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_track'

    def __str__(self):
        return '%s' % self.order+' '+str(self.step)

