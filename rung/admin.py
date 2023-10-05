from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Menu)
admin.site.register(models.AddOn_food)
admin.site.register(models.AddOn_drink)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.discount_coupon)
admin.site.register(models.contact_us)
admin.site.register(models.Addon)