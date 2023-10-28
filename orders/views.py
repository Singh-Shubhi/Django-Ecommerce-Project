from django.shortcuts import render,redirect,HttpResponse 
from .forms import OrderForm
from .models import Orders,OrderPet,Payment
from cart.models import Cart
from datetime import datetime
import uuid
import json
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle,Spacer
from reportlab.lib import colors
from django.conf import settings
from django.core.mail import EmailMessage

# Create your views here.
def place_order(request):
    form = OrderForm()
    current_user = request.user
    # print(current_user)
    cart_item = Cart.objects.filter(user=current_user)
    # print(cart_item)
    cart_items_count = cart_item.count()
    total_amount = request.GET.get('totalamount',0.0)
    if cart_items_count <=0:
        return redirect('pet-list')
    if request.method == "POST":
        form = OrderForm(request.POST)
        data = Orders()
        # print(data)
        if form.is_valid():
            # print('inside valid')
            data.user = request.user
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.phone = form.cleaned_data.get('phone')
            data.email = form.cleaned_data.get('email')
            data.address = form.cleaned_data.get('address')
            data.city = form.cleaned_data.get('city')
            data.state = form.cleaned_data.get('state')
            data.country = form.cleaned_data.get('country')
            data.total = total_amount
            data.ip = request.META.get('REMOTE_ADDR')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().fields[-1])[:5]
            orderNumber = f'ORD-{timestamp}.{unique_id}'
            data.order_number = orderNumber
            data.save()

            # return HttpResponse("Temporary Order Created.")
            # print('48',request.user)
            order_object = Orders.objects.get(user=request.user,order_number=orderNumber)
            context = {
                'orders':order_object.pk,
                'order_number':order_object.order_number,
                'cart_item':[item.pk for item in cart_item],
                'total_amount':total_amount
            }

            serialized_data = json.dumps(context)
            redirect_url = reverse('orders:payments')+f'?data={serialized_data}'
            return redirect(redirect_url)
    return render(request,'orders/order_billing.html',{'form':form})



def create_order_pdf(order,cart_items):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,pagesize=letter)
    elements = []
    customer_info = [
        ["Customer Name:",order.user.get_full_name()],
        ["Address:",order.address],
        ["Phone:",order.phone]
    ]

    customer_table =Table(customer_info)
    customer_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BOTTOMPADDING',(0,0),(-1,0),12)
    ]))

    elements.append(customer_table)
    elements.append(Spacer(0,20))
    item_data = [["Item","Quantity","Price","Total"]]

    for item in cart_items:
        item_data.append([item.pet.anml_name,item.quantity,item.pet.anml_price,item.pet.anml_price*item.quantity])

    item_table = Table(item_data,colWidths=[300,70,70,90])
    item_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(1,1),(-1,-1),'CENTER')
    ]))

    elements.append(item_table)
    doc.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content

def send_order_email(order,cart_items):
    subject = "Your Order Details Are Here"
    from_email = settings.DEFAULT_FROM_EMAIL  #LOCAL HOST
    recipient_email  = order.user.email
    email_body = "ThankYou for Placing the Order, Please find the attached invoice for your references."
    pdf_content = create_order_pdf(order,cart_items)
    email = EmailMessage(subject,email_body,from_email,[recipient_email])
    email.content_subtype = "html"
    email.attach("order_details.pdf",pdf_content,"application/pdf")
    email.send(fail_silently=False)


@csrf_exempt
def payments(request):
    context = {}
    if request.method == "POST":
        try:
            raw_data = request.body.decode('utf-8')
            resp = json.loads(raw_data)
            payment = Payment(
                payment_id = resp['id'],
                user = request.user,
                amount_paid = resp['purchase_units'][0]['amount']['value'],
                status = resp['status']
            )
            payment.save()
            last_order_id = Orders.objects.last().id
            Orders.objects.filter(id=last_order_id).update(payment_id=payment)
            order_data = Orders.objects.get(payment_id=payment)
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                orderpet = OrderPet()
                orderpet.order_id = order_data
                orderpet.user = request.user
                orderpet.Payment = payment
                orderpet.pet = item.pet
                orderpet.quantity = item.quantity
                orderpet.pet_price = item.pet.anml_price
                orderpet.is_ordered = True
                orderpet.save()
            send_order_email(order_data,cart_items) # calling the send_order_eamil
            cart_items.delete() #removing cart data.

        except json.JSONDecodeError as e:
            return JsonResponse({'error':str(e)})
    else:
        serialized_data = request.GET.get('data')
        if serialized_data :
            data = json.loads(serialized_data)  #converting the json structure into string
            orders = Orders.objects.get(pk=data['orders'])
            order_number = orders.order_number
            cart_item = Cart.objects.filter(pk__in=data['cart_item'])
            total_amount = data['total_amount']
            context = {
                'orders':orders,
                'order_number':order_number,
                'cart_item':cart_item,
                'total_amount':total_amount
            }

            # return HttpResponse("Sending Data to payment page.....")
    return render(request,"orders/payment_page.html",context)
        