from rest_framework import serializers
from .models import *

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

    def create(self, validated_data):
        menu_data = validated_data.pop('menu')
        menu_germen_data = validated_data.pop('menu_germen')
        food_data = validated_data.pop('food_id')

        menu_instance = Menu.objects.get(id=menu_data['id'])
        menu_germen_instance = Menu_germen.objects.get(id=menu_germen_data['id'])
        food_instance = Addon.objects.get(id=food_data['id'])

        # Assuming you have a model named AddOnFood
        addon_food_instance = AddOn_food.objects.create(
            menu=menu_instance,
            menu_germen=menu_germen_instance,
            food_id=food_instance
        )

        return addon_food_instance
    class Meta:
        model = AddOn_food
        fields = '__all__'

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

class DiscountCouponGermenSerializer(serializers.ModelSerializer):
    class Meta:
        model = discount_coupon_germen
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

class ShopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = shop_time
        fields = '__all__'