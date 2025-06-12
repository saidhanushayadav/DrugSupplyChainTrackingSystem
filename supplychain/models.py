import hashlib
import json
from django.db import models, transaction

class MedicineModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    expiry_date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    qrcode = models.ImageField(upload_to="qrcodes")
    medicine_acceptance_status = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=100)


class OrderModel(models.Model):
    manufacturer = models.CharField(max_length=100)
    medicine = models.ForeignKey('MedicineModel', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    distributor_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50)
    assigned_supplier = models.CharField(max_length=100, null=True, blank=True)
    assigned_pharmacist = models.CharField(max_length=100, null=True, blank=True)
    assigned_distributor = models.CharField(max_length=100, null=True, blank=True)

    # Blockchain Fields
    previous_hash = models.CharField(max_length=64, blank=True, null=True)
    hash_signature = models.CharField(max_length=64, blank=True, unique=True)

    def compute_hash(self, previous_hash):
        data = {
            "manufacturer": self.manufacturer,
            "medicine": self.medicine.id,
            "order_date": self.order_date.isoformat(),
            "quantity": self.quantity,
            "price": str(self.price),
            "distributor_price": str(self.distributor_price),
            "order_status": self.order_status,
            "assigned_supplier": self.assigned_supplier,
            "assigned_pharmacist": self.assigned_pharmacist,
            "assigned_distributor": self.assigned_distributor,
            "previous_hash": previous_hash,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def update_blockchain():
        orders = OrderModel.objects.order_by('id')
        previous_hash = None
        for order in orders:
            order.previous_hash = previous_hash
            order.hash_signature = order.compute_hash(previous_hash)
            previous_hash = order.hash_signature
            order.save()
        print("Blockchain updated successfully!")

    @staticmethod
    def verify_integrity():
        orders = OrderModel.objects.order_by('id')
        previous_hash = None
        for order in orders:
            computed_hash = order.compute_hash(previous_hash)
            if order.hash_signature != computed_hash:
                print(f"Integrity Error: Order {order.id} has been modified!")
                return False
            previous_hash = order.hash_signature
        print("Blockchain integrity verified successfully!")
        return True

    @staticmethod
    def add_order(data):
        with transaction.atomic():
            last_order = OrderModel.objects.order_by('-id').first()
            previous_hash = last_order.hash_signature if last_order else None

            new_order = OrderModel(**data)
            new_order.previous_hash = previous_hash
            new_order.hash_signature = new_order.compute_hash(previous_hash)
            new_order.save()
            print(f"Order {new_order.id} added successfully!")
            OrderModel.update_blockchain()

    @staticmethod
    def update_order(order_id, update_data):
        with transaction.atomic():
            try:
                order = OrderModel.objects.get(id=order_id)
                for key, value in update_data.items():
                    setattr(order, key, value)
                order.save()
                print(f"Order {order_id} updated successfully!")
                OrderModel.update_blockchain()
            except OrderModel.DoesNotExist:
                print(f"Order {order_id} not found!")

    @staticmethod
    def delete_order(order_id):
        with transaction.atomic():
            try:
                OrderModel.objects.get(id=order_id).delete()
                print(f"Order {order_id} deleted successfully!")
                OrderModel.update_blockchain()
            except OrderModel.DoesNotExist:
                print(f"Order {order_id} not found!")


class MessageModel(models.Model):
    message = models.CharField(max_length=500, default="")
    postedby = models.CharField(max_length=500, default="")
    postedto = models.CharField(max_length=500, default="")
    mdate = models.CharField(max_length=500, default="")

class UserModel(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    role = models.CharField(max_length=50)

