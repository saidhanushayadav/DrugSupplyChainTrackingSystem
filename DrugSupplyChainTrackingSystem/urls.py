from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from supplychain.views import registration, login, addMedicine, getMedicines, searchMedicines, updateMedicine, \
    deleteMedicine, postmessage, uploadmessageaction, getmessages, deletemessages, logout, updateMedicineAction, \
    addOrder, addOrderAction, getOrders, deleteOrder, payment, assignOrder, assignOrderAction, updateOrderPrice, \
    updateOrderPriceAction, updateOrderStatus, updateOrderStatusAction, checkBlockchainIntegrity

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='login'),

    path('registration/', TemplateView.as_view(template_name='registration.html'), name='registration'),
    path('regaction/', registration, name='regaction'),

    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('loginaction/', login, name='loginaction'),

    path('add_medicine/',TemplateView.as_view(template_name='addmedicine.html'), name='add_medicine'),
    path('add_medicine_action/',addMedicine, name='add_medicine'),
    path('view_medicines/', getMedicines, name='view_medicines'),
    path('search_medicine/', searchMedicines, name='search_medicine'),
    path('update_medicine/', updateMedicine, name='update_medicine'),
    path('update_medicine_action/', updateMedicineAction, name='update_medicine'),
    path('delete_medicine/', deleteMedicine, name='delete_medicine'),

    path('addorder/', addOrder, name='registration'),
    path('addOrderAction/', addOrderAction, name=''),
    path('getorders/', getOrders, name=''),
    path('deleteOrder/', deleteOrder, name=''),
    path('payment/', payment, name=''),
    path('assignorder/',assignOrder, name=''),
    path('assignorderaction/', assignOrderAction, name=''),
    path('updateorderprice/',updateOrderPrice, name=''),
    path('updateorderpriceaction/', updateOrderPriceAction, name=''),
    path('updateorderstatus/',updateOrderStatus, name=''),
    path('updateorderstatusaction/', updateOrderStatusAction, name=''),

    path('postmessage/', postmessage, name='registration'),
    path('postmessageaction/', uploadmessageaction, name=''),
    path('getmessages/', getmessages, name=''),
    path('deletemessages/', deletemessages, name=''),

    path('verifyblockchain/', checkBlockchainIntegrity, name=''),


    path('logout/',logout, name=''),
]