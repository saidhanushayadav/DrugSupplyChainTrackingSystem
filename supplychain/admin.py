from django.contrib import admin

# Register your models here.
from .models import MedicineModel, OrderModel, MessageModel, UserModel

admin.site.register(MedicineModel)
admin.site.register(OrderModel)
admin.site.register(MessageModel)
admin.site.register(UserModel)
