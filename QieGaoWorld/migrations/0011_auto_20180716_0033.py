# Generated by Django 2.0.7 on 2018-07-15 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QieGaoWorld', '0010_declareresidences_english_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeclareResidences',
            new_name='DeclareBuildings',
        ),
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.CharField(default='%default%police_cases_watch%police_cases_add%declaration_animals%declaration_buildings%declaration_watch%', max_length=2048),
        ),
    ]
