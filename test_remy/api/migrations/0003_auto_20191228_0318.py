# Generated by Django 3.0.1 on 2019-12-28 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_client_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordertrack',
            name='dish',
        ),
        migrations.AlterField(
            model_name='ordertrack',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.OrderDishes'),
        ),
    ]