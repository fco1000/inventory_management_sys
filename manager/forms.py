from django import forms
from .models import (
    Category,
    Customer,
    Product,
    Supplier,
    Transaction,
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['IDNo','name','physical_address','mobile']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['TransactionID','ProductID','Quantity','TransactionAmount']
        

