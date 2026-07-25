from django.shortcuts import render, redirect
from myadmin.models import *


# ========== HOME ==========

def home(request):
    return render(request,'customer/home.html')

def shop(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filter(pname__icontains=query)

    return render(request, 'customer/shop.html', {'products': products, 'query': query}) 

def about(request):
    return render(request,'customer/about.html')

def dashboard(request):
    filter_tag = request.GET.get('filter', 'best')
    products = Product.objects.filter(tag=filter_tag)[:8]
    return render(request, 'customer/dashboard.html', {'products': products, 'filter_tag': filter_tag})

def feedback(request):
    return render(request, 'customer/feedback.html')

def store_feedback(request):
    if 'customer_id' not in request.session:
        return redirect('home')

    mycomment = request.POST['comment']
    myrating = request.POST['rating']
    customer = Customer.objects.get(user_id=request.session['customer_id'])
    Feedback.objects.create(comment=mycomment, rating=myrating, user=customer)
    return redirect('feedback')

def contact(request):
    return render(request, 'customer/contact.html')

def contact_inquiry(request):
    myname = request.POST['name']
    myemail = request.POST['email']
    mycontact = request.POST['contact']
    mysubject = request.POST['subject']
    mymessage = request.POST['message']
    Inquiry.objects.create(
        name=myname, email=myemail, contact=mycontact,
        subject=mysubject, message=mymessage
    )
    return redirect('contact')

def register(request):
    states = State.objects.all()
    cities = City.objects.all()
    areas = Area.objects.all()
    context = {'states': states, 'cities': cities, 'areas': areas}
    return render(request, 'customer/register.html', context)

def store_register(request):
    myname = request.POST['name']
    myemail = request.POST['email']
    mycontact = request.POST['contact']
    myaddress = request.POST['address']
    mygender = request.POST['gender']
    myarea = request.POST['area_id']
    mycity = request.POST['city_id']
    mystate = request.POST['state_id']
    mypassword = request.POST['password']
    myimage = request.FILES.get('image')

    area = Area.objects.get(area_id=myarea)
    city = City.objects.get(city_id=mycity)
    state = State.objects.get(sid=mystate)

    Customer.objects.create(
        name=myname, email=myemail,contact=mycontact, 
        address=myaddress, gender=mygender,area=area, 
        city=city, state=state, password=mypassword, image=myimage
    )
    return redirect('home')

def shop_details(request, p_id):
    product = Product.objects.get(p_id=p_id)
    related_products = Product.objects.filter(cat=product.cat).exclude(p_id=p_id)[:4]
    return render(request, 'customer/shop_details.html', {
        'product': product,
        'related_products': related_products,
    })

# ========== CART ==========

def shopping_cart(request):
    cart = request.session.get('shopping_cart', {})
    cart_items = []
    total = 0
    cleaned_cart = {}

    for key, item in cart.items():
        try:
            product = Product.objects.get(p_id=int(item['p_id']))
            item_total = product.price * item['qty']
            total += item_total
            cart_items.append({
                'key': key,
                'product': product,
                'size': item['size'],
                'color': item['color'],
                'qty': item['qty'],
                'item_total': item_total,
            })
            cleaned_cart[key] = item
        except (Product.DoesNotExist, ValueError, KeyError, TypeError):
            continue

    request.session['shopping_cart'] = cleaned_cart

    return render(request, 'customer/shopping_cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

def add_to_cart(request, p_id):
    size = request.GET.get('size', '')
    color = request.GET.get('color', '')
    quantity = int(request.GET.get('quantity', 1))

    cart = request.session.get('shopping_cart', {})
    key = f"{p_id}_{size}_{color}"

    if key in cart:
        cart[key]['qty'] += quantity
    else:
        cart[key] = {'p_id': p_id, 'size': size, 'color': color, 'qty': quantity}

    request.session['shopping_cart'] = cart
    request.session.modified = True
    return redirect('shopping_cart')


def remove_from_cart(request, key):
    cart = request.session.get('shopping_cart', {})
    key = str(key)
    if key in cart:
        del cart[key]
    request.session['shopping_cart'] = cart
    return redirect('shopping_cart')


def update_cart_qty(request, key, action):
    cart = request.session.get('shopping_cart', {})
    key = str(key)

    if key in cart:
        if action == 'increase':
            cart[key]['qty'] += 1
        elif action == 'decrease':
            cart[key]['qty'] -= 1
            if cart[key]['qty'] <= 0:
                del cart[key]

    request.session['shopping_cart'] = cart
    return redirect('shopping_cart')

def update_cart_all(request):
    cart = request.session.get('shopping_cart', {})

    for key in list(cart.keys()):
        field_name = f'qty_{key}'
        if field_name in request.POST:
            new_qty = int(request.POST[field_name])
            if new_qty <= 0:
                del cart[key]
            else:
                cart[key]['qty'] = new_qty

    request.session['shopping_cart'] = cart
    return redirect('shopping_cart')

# ========== CHECKOUT / ORDER ==========

def checkout(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer = Customer.objects.get(user_id=request.session['customer_id'])
    cart = request.session.get('shopping_cart', {})
    cart_items = []
    total = 0

    for key, item in cart.items():
        product = Product.objects.get(p_id=item['p_id'])
        item_total = product.price * item['qty']
        total += item_total
        cart_items.append({
            'product': product,
            'size': item['size'],
            'color': item['color'],
            'qty': item['qty'],
            'item_total': item_total,
        })

    context = {'customer': customer, 'cart_items': cart_items, 'total': total}
    return render(request, 'customer/checkout.html', context)

# store_order

def store_order(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer = Customer.objects.get(user_id=request.session['customer_id'])
    cart = request.session.get('shopping_cart', {})

    if not cart:
        return redirect('shopping_cart')

    mymethod = request.POST['method']
    if mymethod == 'Online':
        online_method = request.POST.get('online_method', '')
        mymethod = f"Online - {online_method}"

    total = 0
    for key, item in cart.items():
        product = Product.objects.get(p_id=item['p_id'])
        total += product.price * item['qty']

    order = Order.objects.create(amount=total, method=mymethod, user=customer, status='pending')

    for key, item in cart.items():
        product = Product.objects.get(p_id=item['p_id'])
        OrderDetail.objects.create(order=order, product=product, quantity=item['qty'])

    payment = Payment_Details.objects.create(
        order=order,
        payment_method=mymethod,
        payment_id='',
        signature=''
    )

    contact_value = request.POST.get('phone', '').strip()
    pincode_value = request.POST.get('zip', '').strip()

    Billing_details.objects.create(
        first_name=request.POST.get('first_name', ''),
        last_name=request.POST.get('last_name', ''),
        contact=int(contact_value) if contact_value.isdigit() else 0,
        email=request.POST.get('email', ''),
        address1=request.POST.get('address', ''),
        city=request.POST.get('city', ''),
        state=request.POST.get('state', ''),
        pincode=int(pincode_value) if pincode_value.isdigit() else 0,
        payment_details=payment,
        customer=customer,
        order=order,
    )

    request.session['shopping_cart'] = {}
    return redirect('my_orders')


# ========== BLOG ==========

def blog(request):
    return render(request, 'customer/blog.html')

def blog_details(request):
    return render(request, 'customer/blog_details.html')

# ========== CATEGORY PAGES ==========

def mens(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(cat__cat_name='Men')

    if query:
        products = products.filter(pname__icontains=query)

    return render(request, 'customer/mens.html', {'products': products, 'query': query})

def womens(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(cat__cat_name='Women')

    if query:
        products = products.filter(pname__icontains=query)

    return render(request, 'customer/womens.html', {'products': products, 'query': query})

def child(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(cat__cat_name='child')

    if query:
        products = products.filter(pname__icontains=query)

    return render(request, 'customer/child.html', {'products': products, 'query': query})

# ========== MY ORDERS ==========

def my_orders(request):
    customer = Customer.objects.get(user_id=request.session['customer_id'])
    orders = Order.objects.filter(user=customer).order_by('o_id')
    return render(request, 'customer/my_orders.html', {'orders': orders})


def login_page(request):
    return render(request, 'customer/login.html')

def do_login(request):
    myemail = request.POST['email']
    mypassword = request.POST['password']

    try:
        customer = Customer.objects.get(email=myemail, password=mypassword)
        request.session['customer_id'] = customer.user_id
        return redirect('home')
    except Customer.DoesNotExist:
        return render(request, 'customer/login.html', {'error': 'Invalid email or password'})

def logout_page(request):
    request.session.flush()
    return redirect('home')

def clear_cart(request):
    request.session['shopping_cart'] = {}
    return redirect('shopping_cart')