from django.urls import path
from . import views

urlpatterns = [
    path('pets_list_shown/',views.pet_list,name='pet-list'),
    path('cat_list/',views.cat_data,name="catview"),
    path('dog_list/',views.dog_data,name='dogview'),
    path('snake_list/',views.snake_data,name="snakeview"),
    path('pet_details/<int:pk>',views.pet_details,name="petdetail-view"),
    path('search/',views.search_data,name="search-result"),
    path('my_orders/',views.order_history,name="my_orders"),
]


