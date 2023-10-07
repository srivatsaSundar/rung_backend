from django.db import models

class Menu(models.Model):
    title_name = models.CharField(max_length=200, null=True, blank=True)
    title_image = models.ImageField(upload_to='menu_title_images/', null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.title_name:
            existing_menu = Menu.objects.filter(title_name=self.title_name).first()
            if existing_menu:
                self.title_image = existing_menu.title_image
        super().save(*args, **kwargs)

class Addon(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class AddOn_food(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    food = models.ForeignKey(Addon, on_delete=models.CASCADE)

    def __str__(self):
        return self.food.name

class AddOn_drink(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    drink = models.ForeignKey(Addon, on_delete=models.CASCADE)

    def __str__(self):
        return self.drink.name

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('Deliver', 'Deliver'),
        ('Take Away', 'Take Away'),
    ]
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
    total_price = models.IntegerField(default=0)
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=200, null=True, blank=True, choices=order_status_choices)
    
    def __str__(self):
        return self.person_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.menu.name} - Quantity: {self.quantity}"

class discount_coupon(models.Model):
    coupon_code = models.CharField(max_length=200)
    discount_percentage = models.IntegerField(default=0)
    coupon_name= models.CharField(max_length=200)
    coupon_description = models.TextField(null=True, blank=True)
    coupon_expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.coupon_code

class contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name