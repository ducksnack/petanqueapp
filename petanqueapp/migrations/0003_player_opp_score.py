# Generated by Django 3.2.5 on 2022-07-04 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petanqueapp', '0002_auto_20220702_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='opp_score',
            field=models.IntegerField(default=0),
        ),
    ]
