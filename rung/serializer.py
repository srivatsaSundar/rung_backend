from rest_framework import serializers
from .models import Menu, AddOn_food, AddOn_drink, Order, discount_coupon, contact_us

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class AddOnFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn_food
        fields = '__all__'

class AddOnDrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn_drink
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = discount_coupon
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact_us
        fields = '__all__'
