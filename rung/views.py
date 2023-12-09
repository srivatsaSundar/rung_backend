# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Menu, AddOn_food, AddOn_drink, Order,discount_coupon, contact_us,Addon,Menu_germen,countrycode,holiday_notes
from .serializer import *
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

@api_view(['GET'])
def all_values(request):
    menus = Menu.objects.all()
    serializer = MenuSerializerView(menus, many=True)
    menus_germen = Menu_germen.objects.all()
    serializer_germen = MenuGermenSerializerView(menus_germen, many=True)
    postal_codes = countrycode.objects.all()
    serializer_codes = CountryCodeSerializer(postal_codes, many=True)
    return Response({'menu':serializer.data,'menu_germen':serializer_germen.data,'postal_codes':serializer_codes.data})

@api_view(['GET'])
def holiday(request):
    value=holiday_notes.objects.all()
    serializer = HolidaySerializer(value, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_holiday(request,value=None):
    if value:
        menu=holiday_notes.objects.get(start_data=value)
        serializer=HolidaySerializer(menu, data=request.data, partial=True)
    else:
        serializer = HolidaySerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_menu(request,value=None):
    if value:
        menu=Menu.objects.get(name=value)
        serializer=MenuSerializerView(menu, data=request.data, partial=True)
    else:
        serializer = MenuSerializerView(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_menu_germen(request,value=None):
    if value:
        menu=Menu_germen.objects.get(name=value)
        serializer=MenuGermenSerializerView(menu, data=request.data, partial=True)
    else:
        serializer = MenuGermenSerializerView(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_addon_food(request,value=None):
    if value:
        menu=AddOn_food.objects.get(name=value)
        serializer=AddOnFoodSerializer(menu, data=request.data, partial=True)
    else:
        serializer = AddOnFoodSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_addon_drink(request,value=None):
    if value:
        menu=AddOn_drink.objects.get(name=value)
        serializer=AddOnDrinkSerializer(menu, data=request.data, partial=True)
    else:
        serializer = AddOnDrinkSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_postal_code(request, postal_code=None):
    if postal_code:
        # Update availability if postal_code is provided
        instance = countrycode.objects.get(postal_code=postal_code)
        serializer = CountryCodeSerializer(instance, data=request.data, partial=True)
    else:
        # Add a new postal code if postal_code is not provided
        serializer = CountryCodeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Data successfully processed.'}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
