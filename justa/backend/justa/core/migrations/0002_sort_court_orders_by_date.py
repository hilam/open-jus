# Generated by Django 2.1.5 on 2019-01-18 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_create_court_order_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courtorder',
            options={'ordering': ('-date', 'name')},
        ),
    ]
