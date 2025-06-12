from django.shortcuts import render, redirect
from .models import MedicineModel, OrderModel, MessageModel, UserModel
from .forms import MedicineForm, MessageForm, RegistrationForm, LoginForm
from .service import findMedicineById, getMedicinesBySearchkeyWord, \
    findOrderById, getAllOrders, getOrdersByUserType, getMedicineByUserType
from datetime import datetime

# User Management
def registration(request):

    status = False

    if request.method == "POST":
        # Get the posted form
        registrationForm = RegistrationForm(request.POST)

        if registrationForm.is_valid():

            regModel = UserModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]
            regModel.role = registrationForm.cleaned_data["role"]

            users = UserModel.objects.filter(username=regModel.username)

            if len(users)>0:
                status = False
            else:
                try:
                    regModel.save()
                    status = True
                except Exception as e:
                    status = False

        if status:
            return render(request, 'login.html', {"message": "Registred Successfully"})
        else:
            return render(request, 'registration.html', {"message": "User Email All Ready Exist"})

    return render(request, 'registration.html', {"message": "Registration Failed"})


def login(request):

    if request.method == "GET":
        # Get the posted form
        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            print(uname,upass)
            if uname == "admin" and upass == "admin":
                request.session['username'] = "admin"
                request.session['role'] = "admin"
                print("admin")
                return render(request, "medicines.html", {"medicines":MedicineModel.objects.all()})

            else:
                print("user")
                user = UserModel.objects.get(username=uname, password=upass)
                if user is not None:
                    print("if")
                    request.session['username'] = uname
                    request.session['role'] = user.role

                    if request.session['role']=="manufacturer" or request.session['role']=="distributor":
                        print("if 1")
                        return render(request, 'medicines.html', {"medicines": getMedicineByUserType(request.session['username'],request.session['role'])})

                    elif request.session['role']=="distributor":
                        return render(request, 'medicines.html')

                    elif request.session['role']=="supplier" or request.session['role']=="pharmacist":
                        print("else 1")
                        return render(request, 'orders.html', {"orders": getOrdersByUserType(request.session['username'], request.session['role'])})
                else:
                    print("else")
                    return render(request, 'index.html', {"message": "Invalid username or Password"})
        else:
            print("invalid form")
            return render(request, 'index.html', {"message": "Invalid Form"})
    else:
        print("invalid request")
        return render(request, 'index.html', {"message": "Invalid Request"})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, "index.html")
#-----------------------------------------------------------------------------------------------------
def addMedicine(request):

    medicineForm = MedicineForm(request.POST)

    if medicineForm.is_valid():

        MedicineModel(
            name=medicineForm.cleaned_data['name'],
            brand = medicineForm.cleaned_data['brand'],
            expiry_date = medicineForm.cleaned_data['expiry_date'],
            description = medicineForm.cleaned_data['description'],
            price = medicineForm.cleaned_data['price'],
            quantity = medicineForm.cleaned_data['quantity'],
            medicine_acceptance_status="pending",
            manufacturer=request.session['username']
        ).save()
        return render(request, 'medicines.html', {"medicines": getMedicineByUserType(request.session['username'],request.session['role'])})
    else:
        return render(request, 'addmedicine.html', {"message": "Medicine Adding Failed"})

def getMedicines(request):
    return render(request, 'medicines.html', {"medicines": getMedicineByUserType(request.session['username'],request.session['role'])})

def getMedicineById(request):
    return render(request, 'medicines.html', {"medicines":MedicineModel.objects.filter(id=request.GET['id'])})

def deleteMedicine(request):
    MedicineModel.objects.filter(id=request.GET['id']).delete()
    return render(request, 'medicines.html', {"medicines": getMedicineByUserType(request.session['username'],request.session['role'])})

def updateMedicine(request):
    return render(request, 'updatemedicine.html', {"id":request.GET['id'],"updatetype":request.GET['updatetype']})

def updateMedicineAction(request):

    if request.GET['updatetype']=="price":
        MedicineModel.objects.filter(id=request.GET['id']).update(price = request.GET['price'],quantity=request.GET['quantity'])

    elif request.GET['updatetype']=="medicine_acceptance_status":
        MedicineModel.objects.filter(id=request.GET['id']).update(medicine_acceptance_status = request.GET['status'])

    return render(request, 'medicines.html',
                  {"medicines": getMedicineByUserType(request.session['username'], request.session['role'])})

def searchMedicines(request):
    return render(request, 'medicines.html', {"medicines": getMedicinesBySearchkeyWord(request.GET['keyword'])})
#=======================================================================================================================
def postmessage(request):
    postedto = request.GET['postedto']
    return render(request, "postmessage.html", {"postedto":postedto})

def uploadmessageaction(request):

    messageForm = MessageForm(request.GET)
    uname = request.session['username']

    if messageForm.is_valid():

        message = messageForm.cleaned_data['message']
        postedto = messageForm.cleaned_data['postedto']

        postedby = uname
        mdate = datetime.now()

        MessageModel(message=message,postedby=postedby,postedto=postedto,mdate=mdate).save()

        return render(request, "messages.html", {"messages":MessageModel.objects.filter(postedto=uname)})

    else:
        return render(request, "postmessage.html", {"messages":"invalid form"})

def getmessages(request):
    uname = request.session['username']
    return render(request, "messages.html", {"messages": MessageModel.objects.filter(postedto=uname)})

def deletemessages(request):

    messageid=request.GET['messageid']

    MessageModel.objects.get(id=messageid).delete()

    uname = request.session['username']
    return render(request, "messages.html", {"messages": MessageModel.objects.filter(postedto=uname)})
#======================================================================================
#Order Management
def addOrder(request):
    return render(request, 'placeorder.html',{"medicine_id":request.GET['id']})

def payment(request):

    return render(request, 'payment.html',{
        "medicine_id":request.GET['medicine_id'],
        "price": findMedicineById(request.GET['medicine_id']).price*int(request.GET['quantity']),
        "quantity": request.GET['quantity']
    })

def addOrderAction(request):

    OrderModel.add_order({
        "manufacturer":findMedicineById(request.GET['medicine_id']).manufacturer,
        "medicine":findMedicineById(request.GET['medicine_id']),
        "order_date":datetime.now(),
        "quantity":request.GET['quantity'],
        "price":request.GET['price'],
        "order_status":"Pending",
        "distributor_price":0.0,
        "assigned_distributor":request.session['username']
    })

    return render(request, 'orders.html',{"orders": getOrdersByUserType(request.session['username'], request.session['role'])})

def getOrders(request):
    return render(request, 'orders.html',{"orders": getOrdersByUserType(request.session['username'], request.session['role'])})

def getOrderById(request):
    return render(request, 'orders.html', {"orders":OrderModel.objects.filter(id=request.GET['id'])})

def deleteOrder(request):
    OrderModel.delete_order(request.GET['id'])
    return render(request, 'orders.html', {"orders":getAllOrders()})

def updateOrderPrice(request):
    return render(request, 'updateorderprice.html', {"id":findOrderById(request.GET['id']).id})

def updateOrderPriceAction(request):
    print(len(OrderModel.objects.filter(id=request.GET['id'])))
    print(request.GET['id'],request.GET['distibutor_price'])

    OrderModel.update_order(request.GET['id'], {"distributor_price": request.GET['distibutor_price']})
    return render(request, 'orders.html',{"orders": getOrdersByUserType(request.session['username'], request.session['role'])})

def updateOrderStatus(request):
    return render(request, 'updateorderstatus.html', {"id":findOrderById(request.GET['id']).id})

def updateOrderStatusAction(request):
    OrderModel.update_order(request.GET['id'], {"order_status": request.GET['order_status']})
    return render(request, 'orders.html',{"orders": getOrdersByUserType(request.session['username'], request.session['role'])})

def assignOrder(request):
    return render(request, 'assignorder.html', {"id":request.GET['id'],"users":UserModel.objects.all()})

def assignOrderAction(request):

    OrderModel.update_order(request.GET['id'],
                            {
                                "assigned_supplier": request.GET['supplier'],
                                "assigned_pharmacist":request.GET['pharmacist'],
                            })

    return render(request, 'orders.html',{"orders": getOrdersByUserType(request.session['username'], request.session['role'])})

def checkBlockchainIntegrity(request):
    is_valid = OrderModel.verify_integrity()
    return render(request, 'orders.html',
                  {"orders": getOrdersByUserType(request.session['username'], request.session['role']),
                   "message": "✅ Blockchain is valid" if is_valid else "❌ Blockchain integrity compromised!"})
