from django.db import models
from PETSAPP.models import PetsDetails
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=100,blank=True)
    pet = models.ForeignKey(PetsDetails,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalprice = models.FloatField(default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_tbl'
