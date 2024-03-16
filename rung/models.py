from django.db import models

class Menu(models.Model):
    title_name = models.CharField(max_length=200, null=True, blank=True)
    title_image = models.ImageField(upload_to='menu_title_images/', null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description_1 = models.CharField(max_length=200)
    description_2 = models.CharField(max_length=200,null=True,blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.title_name:
            existing_menu = Menu.objects.filter(title_name=self.title_name).first()
            if existing_menu:
                self.title_image = existing_menu.title_image
        super().save(*args, **kwargs)

class Menu_germen(models.Model):
    title_name = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(default=0,null=True)
    description_1 = models.CharField(max_length=200,null=True)
    description_2 = models.CharField(max_length=200,null=True,blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Addon(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class AddOn_food(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_germen = models.ForeignKey(Menu_germen, on_delete=models.CASCADE,null=True)
    food = models.ForeignKey(Addon, on_delete=models.CASCADE)

    def __str__(self):
        return self.food.name

class AddOn_drink(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_germen = models.ForeignKey(Menu_germen, on_delete=models.CASCADE,null=True)
    drink = models.ForeignKey(Addon, on_delete=models.CASCADE)

    def __str__(self):
        return self.drink.name

class Order(models.Model):
    order_status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    person_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    coupon_code = models.CharField(max_length=200, null=True, blank=True)
    total_price = models.FloatField(default=0)
    delivery_option = models.CharField(max_length=20)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=200, null=True, blank=True, choices=order_status_choices)
    cart= models.CharField(max_length=1000,null=True,blank=True)
    coupon_code_amount=models.CharField(max_length=1000,null=True,blank=True)
    delivery_charges=models.CharField(max_length=1000,null=True,blank=True)
    mail_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return self.person_name

class discount_coupon(models.Model):
    coupon_code = models.CharField(max_length=200)
    discount_percentage = models.IntegerField(default=0)
    coupon_name= models.CharField(max_length=200)
    coupon_description = models.TextField(null=True, blank=True)
    coupon_expiry_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code
    
class discount_coupon_germen(models.Model):
    coupon_code = models.CharField(max_length=200)
    discount_percentage = models.IntegerField(default=0)
    coupon_name= models.CharField(max_length=200)
    coupon_description = models.TextField(null=True, blank=True)
    coupon_expiry_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code

class contact_us(models.Model):
    date= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class countrycode(models.Model):
    postal_code = models.CharField(max_length=200)
    price= models.FloatField(default=0,null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.postal_code
    
class holiday_notes(models.Model):
    start_data = models.DateTimeField(null=True, blank=True)
    end_data = models.DateTimeField(null=True, blank=True)
    holiday_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.start_data
    
class shop_time(models.Model):
    shop_opening_time = models.TimeField(null=True, blank=True)
    shop_closing_time = models.TimeField(null=True, blank=True)
    shop_delivery_opening_time = models.TimeField(null=True, blank=True)
    shop_delivery_closing_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.start_data