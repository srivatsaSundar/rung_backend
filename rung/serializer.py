from rest_framework import serializers
from .models import Menu, AddOn_food, AddOn_drink, Order, discount_coupon, contact_us,Addon,Menu_germen,countrycode,holiday_notes

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name'  ]

class MenuSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuGermenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_germen
        fields = ['name'  ]

class MenuGermenSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Menu_germen
        fields = '__all__'
class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ['name', 'price']

class AddOnFoodSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    menu_germen = MenuGermenSerializer()
    food = AddonSerializer()

    class Meta:
        model = AddOn_food
        exclude = ['id']

class AddOnDrinkSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    menu_germen = MenuGermenSerializer()
    drink = AddonSerializer()

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

class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = countrycode
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = holiday_notes
        fields = '__all__'