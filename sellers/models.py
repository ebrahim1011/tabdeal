from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=200)
    credit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('increase', 'Increase'),
        ('decrease', 'Decrease')
    )
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - Amount: {self.amount}"


class Phone(models.Model):
    number = models.CharField(max_length=11, unique=True)
    charge = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return self.number
