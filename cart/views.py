from django.shortcuts import render,redirect
from .models import Cart
from PETSAPP.models import PetsDetails
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def add_to_cart(request,id):
    cart_id = request.session.session_key
    if cart_id == None:
        cart_id = request.session.create()
    pet_data = PetsDetails.objects.get(id=id)
    price = pet_data.anml_price 
    user_data = request.user
    Cart(cart_id=cart_id,pet=pet_data,user=user_data,totalprice=price).save()
    messages.success(request,"Item added successfully")
    return redirect('/')

def cart_views1(request):
    all_items = Cart.objects.filter(user=request.user)
    flag = all_items.exists()
    return render(request,'cart/cart.html',{'items':all_items, 'flag':flag})


def delete_cart(request,id):
    cart_item_delete = Cart.objects.get(id=id)
    cart_item_delete.delete()
    messages.success(request,'Item removed from cart successfully')
    return redirect('cart-view')

def update_cart(request,id):
    p = request.POST.get('price')
    q = request.POST.get('qty')
    p_id = request.POST.get('id')
    total_price = float(p) * int(q)
    Cart.objects.filter(id=p_id).update(quantity=q,totalprice=total_price)
    return JsonResponse({'status':True,'totalprice':total_price})
