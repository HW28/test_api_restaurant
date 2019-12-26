# Generated by Django 3.0.1 on 2019-12-22 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
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
