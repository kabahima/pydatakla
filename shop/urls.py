from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Shop listing and filtering
    path('', views.shop, name='shop'),
    
    # Product detail
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart operations
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_cart_item'),
    
    # Featured products widget
    path('featured/', views.featured_products, name='featured_products'),

    # Checkout / Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
