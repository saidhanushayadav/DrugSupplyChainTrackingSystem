from django.forms import Form, CharField, FileField, PasswordInput, IntegerField, DecimalField, DateField

class RegistrationForm(Form):
    username = CharField(max_length=50)
    name = CharField(max_length=50)
    password = CharField(widget=PasswordInput())
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    role = CharField(max_length=50)

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class MedicineForm(Form):
    name = CharField(max_length=100)
    brand = CharField(max_length=100)
    expiry_date = DateField()
    description = CharField(max_length=5000)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField()

class MessageForm(Form):
    message=CharField(max_length=500)
    postedto=CharField(max_length=500)
