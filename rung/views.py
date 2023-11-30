# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Menu, AddOn_food, AddOn_drink, Order,discount_coupon, contact_us,Addon,Menu_germen,countrycode
from .serializer import MenuSerializerView, AddOnFoodSerializer, AddOnDrinkSerializer, OrderSerializer, DiscountCouponSerializer, ContactUsSerializer,MenuGermenSerializerView,CountryCodeSerializer
from .mail_utils import schedule_order_email

@api_view(['GET'])
def menu_list(request):
    # if request.method == 'GET':
        menus = Menu.objects.filter(available=True)
        serializer = MenuSerializerView(menus, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def menu_list_germen(request):
    # if request.method == 'GET':
        menus_germen = Menu_germen.objects.filter(available=True)
        serializer = MenuGermenSerializerView(menus_germen, many=True)
        return Response(serializer.data)


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

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        order = serializer.instance  # Get the created order instance
        # Check if mail_sent is False and schedule the email
        if not order.mail_sent:
            schedule_order_email(order)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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

@api_view(['GET'])
def postal_code(request):
    postal_codes = countrycode.objects.filter(available=True)
    serializer = CountryCodeSerializer(postal_codes, many=True)
    return Response(serializer.data)

