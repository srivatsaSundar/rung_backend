from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializer import *
from .mail_utils import schedule_order_email,schedule_contact_email
import json 

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
        order = serializer.instance
        if not order.mail_sent:
            schedule_order_email(order)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_list(request):
    orders=Order.objects.all()
    serializers=OrderSerializer(orders,many=True)
    return Response(serializers.data)

@api_view(['DELETE'])
def delete_order_list(request,cart,delivery_date,person_name):
    try:
        holiday_instance = Order.objects.get(cart=cart,delivery_date=delivery_date,person_name=person_name)
        holiday_instance.delete()
        return Response({'message': 'Order data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except holiday_notes.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def discount_coupon_list(request):
    # if request.method == 'GET':
        discount_coupons = discount_coupon.objects.all()
        serializer = DiscountCouponSerializer(discount_coupons, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def discount_coupon_list_germen(request):
    # if request.method == 'GET':
        discount_coupons = discount_coupon.objects.all()
        serializer = DiscountCouponGermenSerializer(discount_coupons, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_contact_us(request):
    serializer = ContactUsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        contact_us = serializer.instance
        schedule_contact_email(contact_us)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_contact_us(request):
    contact = contact_us.objects.all()
    serializer = ContactUsSerializer(contact, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_contact_us(request,message):
    try:
        holiday_instance = contact_us.objects.get(message=message)
        holiday_instance.delete()
        return Response({'message': 'contact us data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except holiday_notes.DoesNotExist:
        return Response({'error': 'contact us not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def postal_code(request):
    postal_codes = countrycode.objects.filter(available=True)
    serializer = CountryCodeSerializer(postal_codes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def view_addon(request):
    add_on=Addon.objects.all()
    serializer_add_on=AddonSerializer(add_on,many=True)
    return Response(serializer_add_on.data)

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
def add_holiday(request, value=None):
    try:
        if value is not None:
            # Check if a record with the provided start date exists
            instance = holiday_notes.objects.get(start_data=value)
            return Response({'message': 'Holiday data already exists.'}, status=status.HTTP_200_OK)

        # If value is None, check the request data for the start date
        start_data = request.data.get('start_data')
        if start_data is None:
            return Response({'error': 'Start date is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided start date exists
        instance = holiday_notes.objects.get(start_data=start_data)
        return Response({'message': 'Holiday data already exists.'}, status=status.HTTP_200_OK)

    except holiday_notes.DoesNotExist:
        # If the record doesn't exist, create a new one
        serializer = HolidaySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'New holiday data successfully added.'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_holiday(request, start_data):
    try:
        holiday_instance = holiday_notes.objects.get(start_data=start_data)
        holiday_instance.delete()
        return Response({'message': 'Holiday data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except holiday_notes.DoesNotExist:
        return Response({'error': 'Holiday data not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_menu(request, value=None):
    try:
        if value is not None:
            # Check if a record with the provided name exists
            instance = Menu.objects.get(name=value)
            serializer = MenuSerializerView(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If value is None, check the request data for the name
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided name exists
        instance = Menu.objects.filter(name=name).first()

        if instance:
            # If the record exists, update it
            serializer = MenuSerializerView(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = MenuSerializerView(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New menu data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def menu_availability(request,name):
    try:
        instance = Menu.objects.get(name=name)
    except Menu.DoesNotExist:
        return Response({'error': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MenuSerializerView(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Availability successfully updated.'}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_menu(request, name):
    try:
        menu_instance = Menu.objects.get(name=name)
        menu_instance.delete()
        return Response({'message': 'Menu data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Menu.DoesNotExist:
        return Response({'error': 'Menu data not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_menu_germen(request, value=None):
    try:
        if value is not None:
            # Check if a record with the provided name exists
            instance = Menu_germen.objects.get(name=value)
            serializer = MenuGermenSerializerView(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If value is None, check the request data for the name
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided name exists
        instance = Menu_germen.objects.filter(name=name).first()

        if instance:
            # If the record exists, update it
            serializer = MenuGermenSerializerView(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = MenuGermenSerializerView(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New menu data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def menu_availability_germen(request, name):
    try:
        instance = Menu_germen.objects.get(name=name)
    except Menu_germen.DoesNotExist:
        return Response({'error': 'Menu not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MenuGermenSerializerView(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Availability successfully updated.'}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_menu_germen(request, name):
    try:
        menu_instance = Menu_germen.objects.get(name=name)
        menu_instance.delete()
        return Response({'message': 'Menu data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Menu_germen.DoesNotExist:
        return Response({'error': 'Menu data not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def add_addon(request, value=None):
    try:
        if value is not None:
            # Check if a record with the provided name exists
            instance = Addon.objects.get(name=value)
            serializer = AddonSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If value is None, check the request data for the name
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided name exists
        instance = Addon.objects.filter(name=name).first()

        if instance:
            # If the record exists, update it
            serializer = AddonSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Menu data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = AddonSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New menu data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_add_on(request, name):
    try:
        menu_instance = Addon.objects.get(name=name)
        menu_instance.delete()
        return Response({'message': 'Menu data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Addon.DoesNotExist:
        return Response({'error': 'Menu data not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_addon_food(request):
    try:
        data = json.loads(request.body)
        menu_data = data.get('menu')
        menu_germen_data = data.get('menu_germen')
        addon_data = data.get('addon')

        # Ensure that the keys in data match the field names of your models
        if isinstance(menu_data,str):
            menu_instances = Menu.objects.filter(name=menu_data)
        else:
            menu_instances = Menu.objects.filter(**menu_data)
        if isinstance(menu_germen_data,str):
            menu_germen_instances = Menu_germen.objects.filter(name=menu_germen_data)
        else:
            menu_germen_instances = Menu_germen.objects.filter(**menu_germen_data)
        if isinstance(addon_data,str):
            addon_instances = Addon.objects.filter(name=addon_data)
        else:
            addon_instances = Addon.objects.filter(**addon_data)

        menu_id = menu_instances.first().id
        menu_germen_id = menu_germen_instances.first().id
        addon_id = addon_instances.first().id

        serializer = AddOn_food.objects.create(menu_id=menu_id,
             menu_germen_id=menu_germen_id,
            food_id=addon_id)
        serializer.save()
        response_data = {'message': 'New menu data successfully added.'}
        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("Exception:", e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           
@api_view(['DELETE'])
def delete_addon_food(request, id):
    try:
        menu_instance = AddOn_food.objects.get(id=id)
        menu_instance.delete()
        return Response({'message': 'Menu data deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except AddOn_food.DoesNotExist:
        return Response({'error': 'Menu data not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_postal_code(request, postal_code=None):
    try:
        if postal_code is not None:
            # Check if a record with the provided postal code exists
            instance = countrycode.objects.filter(postal_code=postal_code).first()
            serializer = CountryCodeSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Postal code data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If postal_code is None, check the request data for the postal code
        postal_code_value = request.data.get('postal_code')
        if postal_code_value is None:
            return Response({'error': 'Postal code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided postal code exists
        instance = countrycode.objects.filter(postal_code=postal_code_value).first()

        if instance:
            # If the record exists, update it
            serializer = CountryCodeSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Postal code data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = CountryCodeSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New postal code data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def postal_change_availability(request, postal_code):
    try:
        instance = countrycode.objects.get(postal_code=postal_code)
    except countrycode.DoesNotExist:
        return Response({'error': 'Postal code not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CountryCodeSerializer(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Availability successfully updated.'}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_postal_code(request, postal_code):
    try:
        instance = countrycode.objects.get(postal_code=postal_code)
    except countrycode.DoesNotExist:
        return Response({'error': 'Postal code not found.'}, status=status.HTTP_404_NOT_FOUND)

    instance.delete()
    response_data = {'message': 'Postal code successfully deleted.'}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def discount_coupon_list(request):
    # if request.method == 'GET':
        discount_coupons = discount_coupon.objects.all()
        serializer = DiscountCouponSerializer(discount_coupons, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_discount_coupon(request,coupon_code=None):
    try:
        if coupon_code is not None:
            # Check if a record with the provided coupon code exists
            instance = discount_coupon.objects.filter(coupon_code=coupon_code).first()
            serializer = DiscountCouponSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Coupon data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # If coupon_code is None, check the request data for the coupon code
        coupon_code_value = request.data.get('coupon_code')
        if coupon_code_value is None:
            return Response({'error': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a record with the provided coupon code exists
        instance = discount_coupon.objects.filter(coupon_code=coupon_code_value).first()

        if instance:
            # If the record exists, update it
            serializer = DiscountCouponSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Coupon data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = DiscountCouponSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New coupon data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_discount_coupon(request, coupon_code):
    try:
        instance = discount_coupon.objects.get(coupon_code=coupon_code)
    except discount_coupon.DoesNotExist:
        return Response({'error': 'Coupon code not found.'}, status=status.HTTP_404_NOT_FOUND)

    instance.delete()
    response_data = {'message': 'Coupon code successfully deleted.'}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def discount_coupon_availability(request, coupon_code):
    try:
        instance = discount_coupon.objects.get(coupon_code=coupon_code)
    except discount_coupon.DoesNotExist:
        return Response({'error': 'Coupon code not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DiscountCouponSerializer(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Availability successfully updated.'}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def shop_time_list(request):
    shop_times = shop_time.objects.all()
    serializer = ShopTimeSerializer(shop_times, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_shop_time(request, value=None):
    try:
        if value is not None:
            # Check if a record with the provided name exists
            instance = shop_time.objects.filter(id=value).first()
            serializer = ShopTimeSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Shop time data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If value is None, check the request data for the name
        name = request.data.get('id')
        if name is None:
            return Response({'error': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided name exists
        instance = shop_time.objects.filter(id=name).first()

        if instance:
            # If the record exists, update it
            serializer = ShopTimeSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Shop time data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['GET'])

@api_view(['POST'])
def add_discount_coupon_germen(request,coupon_code=None):
    try:
        if coupon_code is not None:
            # Check if a record with the provided coupon code exists
            instance = discount_coupon_germen.objects.filter(coupon_code=coupon_code).first()
            serializer = DiscountCouponGermenSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Coupon data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # If coupon_code is None, check the request data for the coupon code
        coupon_code_value = request.data.get('coupon_code')
        if coupon_code_value is None:
            return Response({'error': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a record with the provided coupon code exists
        instance = discount_coupon_germen.objects.filter(coupon_code=coupon_code_value).first()

        if instance:
            # If the record exists, update it
            serializer = DiscountCouponGermenSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'Coupon data updated successfully.'}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the record doesn't exist, create a new one
            serializer = DiscountCouponGermenSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                response_data = {'message': 'New coupon data successfully added.'}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_discount_coupon_germen(request, coupon_code):
    try:
        instance = discount_coupon_germen.objects.get(coupon_code=coupon_code)
    except discount_coupon.DoesNotExist:
        return Response({'error': 'Coupon code not found.'}, status=status.HTTP_404_NOT_FOUND)

    instance.delete()
    response_data = {'message': 'Coupon code successfully deleted.'}
    return Response(response_data, status=status.HTTP_200_OK)