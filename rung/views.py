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
    add_on_food = AddOn_food.objects.all()
    serializer_add_on_food = AddOnFoodSerializer(add_on_food, many=True)
    add_on=Addon.objects.all()
    serializer_add_on=AddonSerializer(add_on,many=True)
    return Response({'menu':serializer.data,'menu_germen':serializer_germen.data,'postal_codes':serializer_codes.data,'add_on':serializer_add_on.data,'add_on_food':serializer_add_on_food.data})

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
def add_on(request, value=None):
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
        menu_data = request.data.get('menu')
        menu_germen = request.data.get('menu_germen')
        addon = request.data.get('addon')
        print(menu_data)
        print(menu_germen)
        print(addon)
        menu_instance = Menu.objects.get(**menu_data)
        menu_id = menu_instance.id
        menu_germen_instance = Menu_germen.objects.get(**menu_germen)
        menu_germen_id = menu_germen_instance.id
        addon_instance = Addon.objects.get(**addon)
        addon_id = addon_instance.id
        print(menu_id)
        print(menu_germen_id)
        print(addon_id)

        serializer = AddOnFoodSerializer(data={
            'menu_id': menu_id,
            'menu_germen_id': menu_germen_id,
            'food_id': addon_id,
            **request.data
        })

        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'New menu data successfully added.'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
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
    existing_instance = countrycode.objects.filter(postal_code=request.data.get('postal_code')).first()

    if existing_instance:
        return Response({'error': 'Postal code already exists.'}, status=status.HTTP_409_CONFLICT)

    serializer = CountryCodeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        response_data = {'message': 'Data successfully added.'}
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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