from django.shortcuts import render
from .models import PetsDetails
from django.http import Http404
from django.db.models import Q
from orders.models import OrderPet

# Create your views here.

def pet_list(request):
    all_products = PetsDetails.objects.all()
    content = {
        'objects': all_products
    }
    return render(request,'PETSAPP/list.html',content)
    

def cat_data(request):
    all_cat_list = PetsDetails.objects.filter(animal_type='CAT')
    dict_cat = {
        'objects': all_cat_list
    }
    return render (request,'PETSAPP/cat_list.html',dict_cat)

def dog_data(request):
    all_dog_list = PetsDetails.objects.filter(animal_type='DOG')
    dict_dog = {
        'objects': all_dog_list
    }
    return render (request,'PETSAPP/dog_list.html',dict_dog)
    
def snake_data(request):
    all_snake_list = PetsDetails.objects.filter(animal_type='SNAKE')
    dict_snake = {
        'objects': all_snake_list
    }
    return render (request,'PETSAPP/snake_list.html',dict_snake)

def pet_details(request,pk):
    all_pets_data = PetsDetails.objects.get(id=pk)
    dict_details = {
        'objects1': all_pets_data
    }
    return render(request,'PETSAPP/pet_details_page.html',dict_details)

def search_data(request):
    if request.method == "GET":
        searched_data = request.GET.get('search')
        if (len(searched_data)==0):
            raise Http404
        else:
            query = (Q(anml_name__icontains=searched_data) | Q(anml_species__icontains=searched_data) | Q(anml_breed__icontains=searched_data))

            result = PetsDetails.objects.filter(query)
            context = {
                'objects': result
            }
            return render(request,"PETSAPP/search.html",context)
    else:
        raise Http404
    

def order_history(request):
    # user = request.user
    query = OrderPet.objects.filter(user=request.user)
    flag = query.exists()
    status_badge_map = {
        'new':'primary',
        'pending':'warning',
        'delivered':'success',
        'cancelled':'danger'
    }

    # Retriving the order along with associated order item

    orders = OrderPet.objects.filter(user=request.user).select_related('order_id','pet').order_by('-order_id__created_at')
    # print(76,orders)

    order_group = {}
    for order in orders:
        order_number = order.order_id.order_number  # order number
        if order_number not in order_group:
            order_group[order_number] = {
                'order_date':order.order_id.created_at.date(),
                'status':order.order_id.status,
                'status_badge_map':status_badge_map.get(order.order_id.status,'secondary'),
                'order_number':order_number,
                'grand_total':0,
                'items':[]
            }

        order_group[order_number]['grand_total']+=order.pet_price
        total_price_per_item = order.quantity * order.pet_price
        order_group[order_number]['items'].append({
                'item_name':order.pet.anml_name,
                'item_price':order.pet_price,
                'quantity':order.quantity,
                'total_price_per_item':total_price_per_item,
        })

    content = {
        'order_group':order_group.values(),
        'flag':flag
    }


    return render(request,'base/order_history.html',content)