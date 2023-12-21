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
    path('menu_availability/<str:name>/', views.menu_availability, name='menu_availability'),
    path('delete_menu/<str:name>/', views.delete_menu, name='delete_menu'),
    path('add_menu_germen/', views.add_menu_germen, name='add_menu_germen'),
    path('menu_availability_germen/<str:name>/', views.menu_availability_germen, name='menu_availability_germen'),
    path('delete_menu_germen/<str:name>/', views.delete_menu_germen, name='delete_menu_germen'),
    path('add_on/', views.add_on, name='add_on'),
    path('delete_add_on/<str:name>/', views.delete_add_on, name='delete_add_on'),
    path('add_addon_food/', views.add_addon_food, name='add_addon_food'),
    path('delete_addon_food/<str:id>/', views.delete_addon_food, name='delete_addon_food'),
    path('add_postal_code/', views.add_postal_code, name='add_postal_code'),
    path('postal_change_availability/<str:postal_code>/', views.postal_change_availability, name='change_availability'),
    path('delete_postal_code/<str:postal_code>/', views.delete_postal_code, name='delete_postal_code'),
    path('holiday/', views.holiday, name='holiday'),
    path('add_holiday/', views.add_holiday, name='add_holiday'),
    path('delete_holiday/<str:start_data>/', views.delete_holiday, name='delete_holiday'),

]