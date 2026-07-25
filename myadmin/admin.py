from django.contrib import admin

# Register your models here.
from .models import (
    State, City, Area, Category, Subcategory,
    Product, Customer, Order, OrderDetail,
    Feedback, Inquiry
)

admin.site.register(State)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Feedback)
admin.site.register(Inquiry)
