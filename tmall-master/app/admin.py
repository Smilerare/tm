from django.contrib import admin
from .models import User,Category,Property,Product,Propertyvalue,Productimage,Review,Order,Orderitem
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Property)
admin.site.register(Product)
admin.site.register(Propertyvalue)
admin.site.register(Productimage)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Orderitem)
