from django.shortcuts import render, redirect, get_object_or_404
from shop.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from shop.forms import RegisterForm, AddressForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(r):

    data = {}
    data['product'] = Product.objects.all()
    data['category'] = Category.objects.all()

    return render(r, 'home.html', data)


def search(r):

    data = {}
    # data['category'] = Category.objects.all()
    data['product'] = Product.objects.filter(name__icontains=r.GET.get('search'))
    if data :
       return render(r, 'search.html', data)
    else:
        return redirect(home)

def loginfun(r):
    form = AuthenticationForm(r.POST or None)
    if r.method == 'POST':
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(r, user)
            return redirect(home)
    data = {}
    data['form'] = form
    return render(r, 'login.html', data)


def register(r):
    form = RegisterForm(r.POST or None)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(loginfun)
    data = {}
    data['form'] = form
    return render(r, 'register.html', data)


def category(r, slug):
    data = {}
    data['category'] = Category.objects.all()
    data['product'] = Product.objects.filter(category__slug=slug)
    return render(r, 'home.html', data)


def single(r, id):
    product = Product.objects.get(id=id)

    return render(r, 'single.html', {'product': product})


@login_required()
def logoutfun(r):

    logout(r)
    return redirect(home)


@login_required()
def addtocart(r, slug):

    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create( user=r.user, ordered=False, item=product)
    order_qs = Order.objects.filter(user=r.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if (order.items.filter(item__slug=slug).exists()):
            order_item.qty += 1
            order_item.save()
        else:
            order.items.add(order_item)
        return redirect(cart)

    else:
        order = Order.objects.create(user=r.user)
        order.items.add(order_item)
        return redirect(cart)


def cart(r):
    data = {}
    
    data['order'] = Order.objects.filter(user=r.user, ordered=False)

    return render(r, 'cart.html', data)


def removeFromcart(r, slug):
    product = get_object_or_404(Product, slug=slug)
    order = Order.objects.get(user=r.user, ordered=False)
    order_item = OrderItem.objects.get(
        user=r.user, ordered=False, item=product)
    if order:
        if (order.items.filter(item__slug=slug).exists()):
            if order_item.qty <= 1:
                order_item.delete()
            else:
                order_item.qty -= 1
                order_item.save()
        return redirect(cart)


def deletefromcart(r, id):
    order_qs = OrderItem.objects.filter(item__id=id)
    order_qs.delete()
    return redirect(cart)


def checkCode(code):
    try:
        coupon = Coupon.objects.get(code=code)
        return True
    except:
        return False


def getCoupon(code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except:
        # invalid coupon
        return redirect(cart)


def addCoupon(r):
    code = r.POST.get('code')

    if checkCode(code):
        coupon = getCoupon(code)
        order = Order.objects.get(user=r.user, ordered=False)
        order.coupon = coupon
        order.save()
        # successfully coupon applied
    return redirect(cart)


def remove_coupon(r):

    order = Order.objects.get(user=r.user, ordered=False)
    order.coupon = None
    order.save()
    # successfully coupon applied
    return redirect(cart)


def chekout(r):
    form = AddressForm(r.POST or None)
    addresses=Address.objects.filter(user=r.user)
    if r.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.user = r.user
            f.save()
            order = Order.objects.get(user=r.user, ordered=False)
            order.address = f
            order.save()
            return redirect(chekout)
    return render(r, 'chekout.html', {'form': form,'address':addresses})

def chekout_with_save_address(r):
    if r.method=="POST":
        address_id = r.POST.get('saved_address')
        address = Address.objects.get(pk=address_id)
        print(r.POST.get('saved_address'))
        order = Order.objects.get(user=r.user, ordered=False)
        order.address = address
        order.save()
        return redirect(pay_now)

def pay_now(r):
    if r.method=='POST':
        order=Order.objects.get(user=r.user,ordered=False)
        order.ordered=True
        order.save()
        return redirect(my_order)
    return render(r,'payment.html')

def my_order(r):
    data = {}
    
    data['orders'] = Order.objects.filter(user=r.user, ordered=True)
    return render(r,'myorder.html',data)

def deletefromOrder(r, id):
    order=Order.objects.get(id=id)
    order.delete()
    return redirect(my_order)