# Generated by Django 5.0 on 2023-12-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_usersubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquizscore',
            name='total_possible_score',
            field=models.IntegerField(default=0),
        ),
    ]