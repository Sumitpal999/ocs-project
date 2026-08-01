from django.urls import path
from customer import views

urlpatterns = [
    # layout
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('shop', views.shop, name='shop'),
    path('about', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('store_feedback/', views.store_feedback, name='store_feedback'),
    path('contact/', views.contact, name='contact'),
    path('contact_inquiry/', views.contact_inquiry, name='contact_inquiry'),
    path('checkout', views.checkout, name='checkout'),
    path('shop-details/<int:p_id>/', views.shop_details, name='shop_details'),
    path('register/', views.register, name='register'),
    path('store-register/', views.store_register, name='store_register'),

    # Products / Categories
    path('mens/', views.mens, name='mens'),
    path('womens/', views.womens, name='womens'),
    path('child/', views.child, name='child'),

    # Cart
    path('add-to-cart/<int:p_id>/', views.add_to_cart, name='add_to_cart'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('remove-from-cart/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-all/', views.update_cart_all, name='update_cart_all'),
    path('update-cart-qty/<str:key>/<str:action>/', views.update_cart_qty, name='update_cart_qty'),

    # Blog
    path('blog', views.blog, name='blog'),
    path('blog_details', views.blog_details, name='blog_details'),

    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),

    path('checkout', views.checkout, name='checkout'),
    path('store-order/', views.store_order, name='store_order'),

    path('login/', views.login_page, name='login'),
    path('do-login/', views.do_login, name='do_login'),
    path('logout/', views.logout_page, name='logout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:p_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:p_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    
]