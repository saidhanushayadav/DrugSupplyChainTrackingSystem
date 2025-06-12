from supplychain.models import MedicineModel, OrderModel, MessageModel

def getMedicineByUserType(username,role):

    if role == "admin":
        return MedicineModel.objects.all()
    if role == "manufacturer":
        return MedicineModel.objects.filter(manufacturer=username)

def getMedicinesBySearchkeyWord(keyword):
    medicines = []
    for medicine in MedicineModel.objects.all():
        if keyword in medicine.name or keyword in medicine.description:
            medicines.append(medicine)
    return medicines

def findMedicineById(id):
    medicine=MedicineModel.objects.get(id=id)
    return medicine

#==========================================================================
def getAllOrders():
    return OrderModel.objects.all()

def getOrdersByUserType(username,role):

    if role == "manufacturer":
        return OrderModel.objects.filter(manufacturer=username)
    elif role == "distributor":
        return OrderModel.objects.filter(assigned_distributor=username)
    elif role == "supplier":
        return OrderModel.objects.filter(assigned_supplier=username)
    elif role == "pharmacist":
        return OrderModel.objects.filter(assigned_pharmacist=username)
    elif role == "admin":
        return OrderModel.objects.all()

from supplychain.models import MedicineModel, OrderModel, MessageModel

def findOrderById(id):
    order = OrderModel.objects.get(id=id)
    return order
