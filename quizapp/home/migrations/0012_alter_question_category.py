# Generated by Django 4.2.11 on 2024-05-03 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='home.category'),
        ),
    ]