from django.db import models
import datetime

class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Clerk(models.Model):
    first_name = models.CharField(max_length=20)

class Receipt(models.Model):
    DEBT = "DE"
    CREDIT = "CE"
    CASH = "CA"
    PAYMENT_METHOD = [
        (DEBT, "Débito"),
        (CREDIT, "Crédito"),
        (CASH, "Dinheiro"),
    ]

    register_date = models.DateField(default=datetime.date.today)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    paid = models.DecimalField(max_digits=5, decimal_places=2)
    change = models.DecimalField(max_digits=5, decimal_places=2)
    payment = models.CharField(choices=PAYMENT_METHOD, max_length=2)
    clerk = models.ForeignKey(Clerk, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(Item)