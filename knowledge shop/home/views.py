from django.shortcuts import render,redirect
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.models import User
from home.models import Contact, Book, Fibuy, Sell
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 


def index(request):
    return render(request, 'index.html')


# return HttpResponse('hhiiiiiiiiii')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')


def sell(request):
    if request.method == "POST":
        id = request.POST.get('id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cate = request.POST.get('cate')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        money = request.POST.get('money')
        year = request.POST.get('year')
        a = Book.objects.get(id=id)
        sell = Sell(address=address, fname=fname, lname=lname, phone=phone, money=money, cate=cate, year=year,prod_id=id)
        a.quant = a.quant - 1
        a.save()
        sell.save()
    return render(request, 'sell.html')


def buy(request):
    bb = Book.objects.all()
    return render(request, 'buy.html', {'bb': bb})


def jee(request):
    je = Book.objects.filter(cat='JEE')
    return render(request, 'jee.html', {'je': je})


def cbse(request):
    cb = Book.objects.filter(cat='CBSE')
    return render(request, 'cbse.html', {'cb': cb})


def state(request):
    st = Book.objects.filter(cat='STATE')
    return render(request, 'state.html', {'st': st})


def engg(request):
    en = Book.objects.filter(cat='ENGG')
    return render(request, 'engg.html', {'en': en})


def defence(request):
    de = Book.objects.filter(cat='DEFENCE')
    return render(request, 'defence.html', {'de': de})


def icse(request):
    ic = Book.objects.filter(cat='ICSE')
    return render(request, 'icse.html', {'ic': ic})


def fibuy(request, id):
    if request.method == "POST":
        id=request.POST.get('id')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        print(id)
        a=Book.objects.get(id=id)
        fibuy = Fibuy(address=address, email=email, phone=phone,prod_id=id)
        print(1)
        fibuy.save()
        a.quant=a.quant-1
        a.save()
        return render(request, 'good.html')

    if request.method == "GET":
        a = Book.objects.get(id=id)
        return render(request, 'fibuy.html', {'a': a})

def final(request):

        return render(request, 'good.html')


def good(request):
    # ic = Icse.objects.all()
    return render(request, 'good.html')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}


    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})


def checkout(request):
    return render(request, 'checkout.html', {})

def updateCart(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    if action == "add":
        cartitem.quantity += 1
        cartitem.save()
    

    return JsonResponse("Cart Updated", safe = False)


def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False)


def user_register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.warning(request,'password does not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request,'username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'email already taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=uname,email=email,password=pass1)
            user.save()
            messages.success(request,'User registered successfully')
            return redirect('login')

        

    return render(request,'login.html')

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request,'User is not registered')
            return redirect('register')
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')   