from django.db import models

# Create your models here.

class PetsDetails(models.Model):
    gender_option = (("Male","Male"),("Female","Female"))
    animal_type_options = (("DOG","DOG"),("CAT","CAT"),("SNAKE","SNAKE"))
    animal_type = models.CharField(max_length=50,choices=animal_type_options)
    anml_gender = models.CharField(max_length=50,choices=gender_option)
    anml_name = models.CharField(max_length=100)
    anml_species = models.CharField(max_length=100)
    anml_breed = models.CharField(max_length=100)
    anml_age = models.IntegerField()
    anml_price = models.FloatField()
    anml_image = models.ImageField(upload_to='media')
    anml_description = models.TextField(max_length=1000)
    