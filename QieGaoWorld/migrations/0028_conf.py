# Generated by Django 2.0.7 on 2018-09-05 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QieGaoWorld', '0027_wenjuanlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]