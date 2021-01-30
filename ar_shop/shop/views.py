from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .forms import CreateUserForm, AuthenticationForm
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .utils import cookieCart, cartData, guestOrder
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def home_page(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    catogeries = Catogery.objects.all()
    context = {"products" : products, "catogeries" : catogeries, "items": items, "order": order}
    return render(request, "home.html", context)

def product_details_page(request, pk):
    data = cartData(request)
    order = data['order']
    items = data['items']
    product = Product.objects.get(title = pk)
    catogeries = Catogery.objects.all()
    images = ProductImage.objects.filter(product = product)
    similarproducts = Product.objects.filter(catogery = product.catogery)
    context = {"product" : product, "images": images, "similarproducts": similarproducts, "catogeries" : catogeries, "items": items, "order": order}
    return render(request, "product-details.html", context)

def shop_page(request, pk):
    data = cartData(request)
    order = data['order']
    items = data['items']
    cat = Catogery.objects.get(name = pk)
    catogeries = Catogery.objects.all()
    products = Product.objects.filter(catogery = cat)
    context = {"products" : products, "catogeries" : catogeries, "items": items, "order": order}
    return render(request, "shop.html", context)

def cart_page(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    catogeries = Catogery.objects.all()
    context = {"items": items, "order": order, "cartItems": cartItems, "catogeries": catogeries}
    return render(request, "cart-page.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    add_to_cart_quantity = data['add_to_cart_quantity']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
	    orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
	    orderItem.quantity = (orderItem.quantity - 1)
    elif action == "add-to-cart":
        orderItem.quantity = (orderItem.quantity + add_to_cart_quantity)

    orderItem.save()

    if (orderItem.quantity <= 0):
	    orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
	    customer = request.user.customer
	    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
	    customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
	    order.complete = True
    order.status = 'Pending'
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        state=data['shipping']['state'],
        city=data['shipping']['city'],
        pincode=data['shipping']['pincode'],
        country=data['shipping']['country'],
        phone=data['form']['phone'],
    )

    CustomerAddress.objects.create(
        customer=customer,
        address=data['shipping']['address'],
        state=data['shipping']['state'],
        city=data['shipping']['city'],
        pincode=data['shipping']['pincode'],
        country=data['shipping']['country'],
        phone=data['form']['phone'],
    )

    return JsonResponse('Payment submitted..', safe=False)

def checkout_page(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    catogeries = Catogery.objects.all()
    country = Country.objects.all()
    customer_address = CustomerAddress.objects.all()
    context = {"items": items, "order": order, "cartItems": cartItems, "catogeries": catogeries, "countries": country, "customer_address_list": customer_address}
    return render(request, "checkout.html", context)

# @unauthenticated_user
# def login_page(request):
#     return render(request,'registration/login.html',{})

@unauthenticated_user
def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})

def about_us_page(request):
    return render(request, "about-us.html", {})

def contact_page(request):
    return render(request, "contact.html", {})
