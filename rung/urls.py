from django.urls import path
from . import views

urlpatterns = [
    path('code/', views.postal_code, name='postal_code'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu_germen/', views.menu_list_germen, name='menu_list_germen'),
    path('add_on_food/', views.add_on_food_list, name='add_on_food_list'),
    path('add_on_drink/', views.add_on_drink_list, name='add_on_drink_list'),
    path('order/', views.create_order, name='create_order'),
    path('discount_coupon/', views.discount_coupon_list, name='discount_coupon_list'),
    path('contact_us/', views.create_contact_us, name='create_contact_us'),
]