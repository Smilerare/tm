# Generated by Django 2.1.7 on 2019-04-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart_ischose'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cartid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
