from django.db import models

# Create your models here.

# 1. State
class State(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=100)

    def _str_(self):
        return self.sname

# 2. City
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def _str_(self):
        return self.city_name

# 3. Area
class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def _str_(self):
        return self.area_name

# 4. Category
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100)

    def _str_(self):
        return self.cat_name

# 5. Subcategory
class Subcategory(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=100)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def _str_(self):
        return self.sub_name

# 6. Product
class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    small_description = models.TextField()
    large_description = models.TextField()
    image = models.ImageField(upload_to='products/')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=200)
    color = models.CharField(max_length=200)

    TAG_CHOICES = [
        ('best', 'Best Seller'),
        ('new', 'New Arrival'),
        ('hot', 'Hot Sale'),
    ]
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='best')

    @property
    def size_list(self):
        return [s.strip() for s in self.size.split(',') if s.strip()]

    @property
    def color_list(self):
        return [c.strip() for c in self.color.split(',') if c.strip()]

    def _str_(self):
        return self.pname

# 7. Customer
class Customer(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='customers/', blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name

# 8. Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    o_id = models.AutoField(primary_key=True)
    odate = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def _str_(self):
        return f"Order #{self.o_id}"

# 9. Order Details
class OrderDetail(models.Model):
    od_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def _str_(self):
        return f"OrderDetail #{self.od_id}"

# 10. Feedback
class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_date = models.DateField(auto_now_add=True)
    comment = models.TextField()
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)

    def _str_(self):
        return f"Feedback by {self.user.name}"

# 11. Inquiry
class Inquiry(models.Model):
    inq_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def _str_(self):
        return f"Inquiry from {self.name}"
    

# Admin
class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def _str_(self):
        return self.username
    
class Payment_Details(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30)
    payment_id = models.TextField()
    signature = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'Payment_Details'



class Billing_details(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.IntegerField()
    email = models.CharField(max_length=50)
    address1 = models.TextField()
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    pincode = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_details = models.ForeignKey(Payment_Details, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing_details'


