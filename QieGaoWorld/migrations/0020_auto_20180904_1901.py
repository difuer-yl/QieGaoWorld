# Generated by Django 2.0.7 on 2018-09-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QieGaoWorld', '0019_menu_wenjuan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='type',
            field=models.IntegerField(),
        ),
    ]