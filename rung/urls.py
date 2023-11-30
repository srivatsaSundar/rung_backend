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
    path('all_values/', views.all_values, name='all_values'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('add_menu_germen/', views.add_menu_germen, name='add_menu_germen'),
    path('add_addon_food/', views.add_addon_food, name='add_addon_food'),
    path('add_addon_drink/', views.add_addon_drink, name='add_addon_drink'),
    path('add_postal_code/', views.add_postal_code, name='add_postal_code'),
]