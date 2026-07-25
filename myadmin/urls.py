from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myadmin import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Category
    path('add-category/', views.add_category, name='add_category'),
    path('store-category/', views.store_category, name='store_category'),
    path('all-category/', views.all_category, name='all_category'),
    path('delete-category/<int:cat_id>/', views.delete_category, name='delete_category'),
    path('edit-category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('update-category/<int:cat_id>/', views.update_category, name='update_category'),

    # Subcategory
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('store-subcategory/', views.store_subcategory, name='store_subcategory'),
    path('all-subcategory/', views.all_subcategory, name='all_subcategory'),
    path('delete-subcategory/<int:sub_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('edit-subcategory/<int:sub_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('update-subcategory/<int:sub_id>/', views.update_subcategory, name='update_subcategory'),

    # Product
    path('add-product/', views.add_product, name='add_product'),
    path('store-product/', views.store_product, name='store_product'),
    path('all-product/', views.all_product, name='all_product'),
    path('delete-product/<int:p_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:p_id>/', views.edit_product, name='edit_product'),
    path('update-product/<int:p_id>/', views.update_product, name='update_product'),

    # Users
    path('all-users/', views.all_users, name='all_users'),

    # Orders
    path('all-orders/', views.all_orders, name='all_orders'),

    # Inquiry
    path('all-inquiry/', views.all_inquiry, name='all_inquiry'),

    # Feedback
    path('all-feedback/', views.all_feedback, name='all_feedback'),
    path('update-order-status/<int:o_id>/', views.update_order_status, name='update_order_status'),
    path('delete-order/<int:o_id>/', views.delete_order, name='delete_order'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)