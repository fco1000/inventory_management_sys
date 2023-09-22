from django.contrib import admin
from .models import Category,Customer,Product,Supplier,Transaction

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Transaction)
