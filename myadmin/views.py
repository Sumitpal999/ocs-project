from django.shortcuts import render, redirect
from myadmin.models import *

# ========== DASHBOARD ==========
def dashboard(request):
    total_users = Customer.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_inquiry = Inquiry.objects.count()
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_inquiry': total_inquiry,
    }
    return render(request, 'myadmin/dashboard.html', context)

# ========== CATEGORY ==========
def add_category(request):
    return render(request, 'myadmin/add_category.html')

def store_category(request):
    cat_name = request.POST['cat_name']
    Category.objects.create(cat_name=cat_name)
    return redirect('all_category')

def all_category(request):
    categories = Category.objects.all()
    return render(request, 'myadmin/all_category.html', {'categories': categories})

def delete_category(request, cat_id):
    Category.objects.get(cat_id=cat_id).delete()
    return redirect('all_category')

def edit_category(request, cat_id):
    cat = Category.objects.get(cat_id=cat_id)
    return render(request, 'myadmin/edit_category.html', {'cat': cat})

def update_category(request, cat_id):
    cat_name = request.POST['cat_name']

    data = {
        'cat_name': cat_name
    }

    Category.objects.update_or_create(pk=cat_id, defaults=data)
    return redirect('all_category')

# ========== SUBCATEGORY ==========
def add_subcategory(request):
    categories = Category.objects.all()
    return render(request, 'myadmin/add_subcategory.html', {'categories': categories})

def store_subcategory(request):
    sub_name = request.POST['sub_name']
    cat_id = request.POST['cat_id']
    cat = Category.objects.get(cat_id=cat_id)
    Subcategory.objects.create(sub_name=sub_name, cat=cat)
    return redirect('all_subcategory')

def all_subcategory(request):
    subcategories = Subcategory.objects.all()
    return render(request, 'myadmin/all_subcategory.html', {'subcategories': subcategories})

def delete_subcategory(request, sub_id):
    Subcategory.objects.get(sub_id=sub_id).delete()
    return redirect('all_subcategory')

def edit_subcategory(request, sub_id):
    sub = Subcategory.objects.get(sub_id=sub_id)
    categories = Category.objects.all()
    return render(request, 'myadmin/edit_subcategory.html', {'sub': sub, 'categories': categories})

def update_subcategory(request, sub_id):
    sub_name = request.POST['sub_name']
    cat = Category.objects.get(cat_id=request.POST['cat_id'])

    data = {
        'sub_name': sub_name,
        'cat': cat
    }

    Subcategory.objects.update_or_create(pk=sub_id, defaults=data)
    return redirect('all_subcategory')

# ========== PRODUCT ==========
def add_product(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'myadmin/add_product.html', {'categories': categories, 'subcategories': subcategories})

def store_product(request):
    pname = request.POST['pname']
    price = request.POST['price']
    small_description = request.POST['small_description']
    large_description = request.POST['large_description']
    image = request.FILES['image']
    cat = Category.objects.get(cat_id=request.POST['cat_id'])
    subcat = Subcategory.objects.get(sub_id=request.POST['sub_id'])
    quantity = request.POST['quantity']
    tag = request.POST.get('tag', 'best')

    sizes = request.POST.getlist('size')
    colors = request.POST.getlist('color')
    size = ', '.join(sizes)
    color = ', '.join(colors)

    Product.objects.create(
        pname=pname, price=price,
        small_description=small_description,
        large_description=large_description,
        image=image, cat=cat, subcat=subcat,
        quantity=quantity, size=size, color=color, tag=tag
    )
    return redirect('all_product')

def all_product(request):
    products = Product.objects.all()
    return render(request, 'myadmin/all_product.html', {'products': products})

def delete_product(request, p_id):
    Product.objects.get(p_id=p_id).delete()
    return redirect('all_product')

def edit_product(request, p_id):
    product = Product.objects.get(p_id=p_id)
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'myadmin/edit_product.html', {'product': product, 'categories': categories, 'subcategories': subcategories})

def update_product(request, p_id):
    pname = request.POST['pname']
    price = request.POST['price']
    small_description = request.POST['small_description']
    large_description = request.POST['large_description']
    cat = Category.objects.get(cat_id=request.POST['cat_id'])
    subcat = Subcategory.objects.get(sub_id=request.POST['sub_id'])
    quantity = request.POST['quantity']
    tag = request.POST.get('tag', 'best')

    sizes = request.POST.getlist('size')
    colors = request.POST.getlist('color')
    size = ', '.join(sizes)
    color = ', '.join(colors)

    data = {
        'pname': pname,
        'price': price,
        'small_description': small_description,
        'large_description': large_description,
        'cat': cat,
        'subcat': subcat,
        'quantity': quantity,
        'size': size,
        'color': color,
        'tag': tag,
    }

    if request.FILES.get('image'):
        data['image'] = request.FILES['image']

    Product.objects.update_or_create(pk=p_id, defaults=data)
    return redirect('all_product')

# ========== USERS ==========
def all_users(request):
    users = Customer.objects.all()
    return render(request, 'myadmin/all_users.html', {'users': users})

# ========== ORDERS ==========
def all_orders(request):
    orders = Order.objects.all()
    return render(request, 'myadmin/all_orders.html', {'orders': orders})

# ========== INQUIRY ==========
def all_inquiry(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'myadmin/all_inquiry.html', {'inquiries': inquiries})

# ========== FEEDBACK ==========
def all_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'myadmin/all_feedback.html', {'feedbacks': feedbacks})

def update_order_status(request, o_id):
    order = Order.objects.get(o_id=o_id)
    order.status = request.POST['status']
    order.save()
    return redirect('all_orders')

def delete_order(request, o_id):
    Order.objects.get(o_id=o_id).delete()
    return redirect('all_orders')