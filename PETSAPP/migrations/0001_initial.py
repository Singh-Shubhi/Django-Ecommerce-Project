# Generated by Django 4.2.2 on 2023-06-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_type', models.CharField(choices=[('DOG', 'DOG'), ('CAT', 'CAT'), ('SNAKE', 'SNAKE')], max_length=50)),
                ('anml_gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50)),
                ('anml_name', models.CharField(max_length=100)),
                ('anml_species', models.CharField(max_length=100)),
                ('anml_breed', models.CharField(max_length=100)),
                ('anml_age', models.IntegerField()),
                ('anml_price', models.FloatField()),
                ('anml_image', models.ImageField(upload_to='media')),
                ('anml_description', models.TextField(max_length=1000)),
            ],
        ),
    ]