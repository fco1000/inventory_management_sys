from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    IDNo = models.IntegerField()
    name = models.CharField(max_length=100,null=True)
    physical_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    TransactionID  = models.IntegerField(null=False)
    
    def __str__(self) -> str:
        return self.user.username
    
class Category(models.Model):
    categoryId = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.categoryId
    
class Supplier(models.Model):
    SupplierID = models.CharField(max_length=100)
    SupplierName = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    ContactEmail = models.EmailField()
    ContactPhone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.SupplierName

class Product(models.Model):
    ProductID = models.BigAutoField(primary_key=True,unique=True)
    ProductName = models.CharField(max_length=50)
    Description = models.TextField(max_length=150)
    CategoryID = models.ForeignKey(Category,on_delete=models.CASCADE)
    SupplierID = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    UnitPrice = models.IntegerField()
    QuantityInStock = models.IntegerField()
    
    def __str__(self):
        return f'{self.ProductID} - {self.ProductName}'

class Transaction(models.Model):
    TransactionID  = models.BigAutoField(primary_key=True,unique=True,null=False)
    ProductID  = models.IntegerField()
    TransactionType  = models.CharField(max_length=100,choices=[('Purchase','Purchase'),('Sale','Sale')])
    TransactionDate = models.DateField(auto_now=True)
    Quantity = models.IntegerField()
    TransactionAmount = models.IntegerField()
    
    def __str__(self):
        return f'Transaction ID{self.TransactionID}-Product {self.ProductID}-Amount {self.TransactionAmount}'