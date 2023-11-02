from rest_framework import serializers
from .models import Menu, AddOn_food, AddOn_drink, Order, discount_coupon, contact_us,Addon,Menu_germen,OrderItem

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
        fields = '__all__'

class AddOnDrinkSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    menu_germen = MenuGermenSerializer()
    drink = AddonSerializer()

    class Meta:
        model = AddOn_drink
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = discount_coupon
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact_us
        fields = '__all__'
