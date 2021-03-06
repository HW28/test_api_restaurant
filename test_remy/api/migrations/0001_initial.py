# Generated by Django 3.0.1 on 2019-12-27 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('surname', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(max_length=25)),
                ('identification_card', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('mail', models.EmailField(max_length=254)),
                ('temporal', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='ClientAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=25)),
                ('postal_code', models.CharField(max_length=5)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Client')),
            ],
            options={
                'db_table': 'client_address',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dish',
            },
        ),
        migrations.CreateModel(
            name='DishTemperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'dish_temperature',
            },
        ),
        migrations.CreateModel(
            name='DishType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'dish_type',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'ingredient',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField()),
                ('deliver_time', models.DateTimeField(blank=True, null=True)),
                ('finish', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('cancel_reason', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Client')),
                ('client_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ClientAddress')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='TimeUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'time_units',
            },
        ),
        migrations.CreateModel(
            name='OrderTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField()),
                ('end', models.BooleanField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
            ],
            options={
                'db_table': 'order_track',
            },
        ),
        migrations.CreateModel(
            name='OrderDishes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
            ],
            options={
                'db_table': 'order_dish',
            },
        ),
        migrations.CreateModel(
            name='DishSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_step', models.IntegerField()),
                ('step', models.TextField()),
                ('time', models.IntegerField()),
                ('ingredients', models.IntegerField(blank=True, null=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
                ('time_units', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TimeUnits')),
            ],
            options={
                'db_table': 'dish_steps',
            },
        ),
        migrations.CreateModel(
            name='DishIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Ingredient')),
            ],
            options={
                'db_table': 'dish_ingredients',
            },
        ),
        migrations.CreateModel(
            name='DishAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temporary', models.BooleanField(default=False)),
                ('release_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
            ],
            options={
                'db_table': 'dish_available',
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='dish_temperature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DishTemperature'),
        ),
        migrations.AddField(
            model_name='dish',
            name='dish_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DishType'),
        ),
        migrations.CreateModel(
            name='ClientDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dish')),
            ],
            options={
                'db_table': 'client_dish',
            },
        ),
    ]
