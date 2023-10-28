from django.contrib import admin
from .models import PetsDetails
from django.utils.html import format_html
from orders.models import Orders,Payment,OrderPet
from cart.models import Cart


class OrderCustom(admin.ModelAdmin):
    list_display = ['user','status']

class PaymentCustom(admin.ModelAdmin):
    list_display = ['payment_id','status']

class DisplayOnPanel(admin.ModelAdmin):
    list_display = ['anml_name','anml_age','anml_species','anml_breed','anml_price','anml_image','display_image','anml_description']
    list_filter = ['anml_gender','animal_type','anml_price']
    search_fields = ['anml_name','anml_gender','animal_type','anml_age']
    list_per_page = 3

    def display_image(self,obj):
        return format_html ('<img src={} height="250" width="250" />',obj.anml_image.url)

# Register your models here.
admin.site.register(PetsDetails,DisplayOnPanel)
admin.site.register(Cart)
admin.site.register(Orders,OrderCustom)
admin.site.register(Payment,PaymentCustom)
admin.site.register(OrderPet)

