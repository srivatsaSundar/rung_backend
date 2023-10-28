# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Menu, AddOn_food, AddOn_drink, Order, OrderItem, discount_coupon, contact_us,Addon,Menu_germen
from .serializer import MenuSerializerView, AddOnFoodSerializer, AddOnDrinkSerializer, OrderSerializer, DiscountCouponSerializer, ContactUsSerializer,MenuGermenSerializerView


@api_view(['GET'])
def menu_list(request):
    # if request.method == 'GET':
        menus = Menu.objects.all()
        add_on_food = AddOn_food.objects.all()
        add_on_drink = AddOn_drink.objects.all()
        serializer = MenuSerializerView(menus, many=True)
        add_on_food_serializer = AddOnFoodSerializer(add_on_food, many=True)
        add_on_drink_serializer = AddOnDrinkSerializer(add_on_drink, many=True)
        data = {
        'menu': serializer.data,
        'add_on_food': add_on_food_serializer.data,
        'add_on_drink': add_on_drink_serializer.data
        }
        return Response(data)

@api_view(['GET'])
def menu_list_germen(request):
    # if request.method == 'GET':
        menus_germen = Menu_germen.objects.all()
        add_on_food = AddOn_food.objects.all()
        add_on_drink = AddOn_drink.objects.all()

        menu_serializer = MenuGermenSerializerView(menus_germen, many=True)
        add_on_food_serializer = AddOnFoodSerializer(add_on_food, many=True)
        add_on_drink_serializer = AddOnDrinkSerializer(add_on_drink, many=True)

        data = {
        'menu': menu_serializer.data,
        'add_on_food': add_on_food_serializer.data,
        'add_on_drink': add_on_drink_serializer.data
        }
        return Response(data)


@api_view(['GET'])
def add_on_food_list(request):
    add_on_food = AddOn_food.objects.all()
    serializer = AddOnFoodSerializer(add_on_food, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def add_on_drink_list(request):
    add_on_drink = AddOn_drink.objects.all()
    serializer = AddOnDrinkSerializer(add_on_drink, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])
def create_order(request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for menu_item in request.data['menu_items']:
                order_item = OrderItem.objects.create(
                    order=order,
                    menu_id=menu_item['id'],
                    quantity=menu_item['quantity']
                )
                order_item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def discount_coupon_list(request):
    # if request.method == 'GET':
        discount_coupons = discount_coupon.objects.all()
        serializer = DiscountCouponSerializer(discount_coupons, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_contact_us(request):
    serializer = ContactUsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
