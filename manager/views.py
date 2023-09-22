from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Transaction,Category,Customer,Product,Supplier
from .forms import CategoryForm,CustomerForm,ProductForm,SupplierForm,TransactionForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from stock import settings
from .filters import CustomerFilter,TransactionFilter

def userCreationView(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
        return render(request,'users/register.html',{'form':form})

@login_required(login_url=settings.LOGIN_URL)   
def userChangeView(request,user):
    form = UserChangeForm(user=user)
    if form.is_valid():
        form.save()
    else:
        return render(request,'users/profile.html')
    
class userLogoutView(LoginRequiredMixin,LogoutView):
    
    def get_success_url(self):
        return reverse('login') 

class userLoginView(LoginView):
    
    def get_success_url(self):
        return reverse('home') 
    

@login_required(login_url=settings.LOGIN_URL)
def homeView(request):
    suppliers = Supplier.objects.count()
    sales = Transaction.objects.filter(TransactionType='Sale').count()
    purchases = Transaction.objects.filter(TransactionType='Purchase').count()
    
    context = {
       'suppliers':suppliers,
       'sales':sales,
       'purchases':purchases, 
    }
    return render(request, 'manager/index.html', context)
    
    
@login_required(login_url=settings.LOGIN_URL)
def customer_view(request):
    customerq = Customer.objects.filter()
    mycustomerFilter = CustomerFilter(request.GET,queryset=customerq)
    customerItems = mycustomerFilter.qs
    
    return render(request,'manager/customers.html',{
        'mycustomerFilter':mycustomerFilter,
        'customerItems':customerItems
        })
   
@login_required(login_url=settings.LOGIN_URL)
def customerUpdateView(request,id):
    customer = Customer.objects.get(id=id)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(id=id,instance=customer)        
        if form.is_valid:
            form.save()
            return redirect('customer')
    else:
        return render(request, 'manager/customer_update.html', {'form':form,'customer':customer})

@login_required(login_url=settings.LOGIN_URL)
def categoryView(request):
    categories = Category.objects.all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        return render(request, 'manager/category.html', {'categories':categories,'form':form})

@login_required(login_url=settings.LOGIN_URL)
def categoryUpdateView(request,id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        return render(request, 'manager/category_update.html', {'form':form,'category':category})
 
@login_required(login_url=settings.LOGIN_URL)
def productView(request):
    products = Product.objects.all()
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        return render(request, 'manager/product.html',{'products':products,'form':form})
   
@login_required(login_url=settings.LOGIN_URL)
def productUpdateView(request,id):
    product = Product.objects.get(ProductID=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)        
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        return render(request, 'manager/product_update.html', {'form':form,'product':product})    

@login_required(login_url=settings.LOGIN_URL)
def purchasesView(request):
    purchases = Transaction.objects.filter(TransactionType='Purchase')
    products = Product.objects.all()
    form = TransactionForm()
    
    purchaseq = Transaction.objects.filter()
    myPurchaseFilter = TransactionFilter(request.GET,queryset=purchaseq)
    purchaseItems = myPurchaseFilter.qs
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)        
        if form.is_valid():            
            
            purchase = form.save(commit=False)
            
            purchase.TransactionType='Purchase'
            purchase.save()
            
            id = purchase.ProductID
            
            quantity = purchase.Quantity
            
            oq = Product.objects.get(ProductID=id)
            original_quantity = oq.QuantityInStock
            original_quantity += quantity
            # Update the QuantityInStock field of the Product object
            oq.QuantityInStock = original_quantity
            oq.save()  # Save the changes to the Product object
            return redirect('purchase')
            
    else:        
        context = {
            'purchases':purchases,
            'form':form,
            'products':products,
            'purchaseItems':purchaseItems,
            'myPurchaseFilter':myPurchaseFilter
            }
        return render(request, 'manager/purchases.html', context)

@login_required(login_url=settings.LOGIN_URL)
def purchaseUpdateView(request,id):
    purchase = Transaction.objects.get(TransactionID = id)
    form = TransactionForm(instance=purchase)
    
    
    if request.method == 'POST':        
        form = TransactionForm(request.POST,instance=purchase )
        
        if form.is_valid:

            former = Product.objects.get(ProductID=purchase.ProductID)
            former_quantity = former.QuantityInStock 
            form.save()
            
            ProductID = form.cleaned_data['ProductID']
            Quantity = form.cleaned_data['Quantity']
            
            og_quantity = Product.objects.get(ProductID=ProductID)
            object = Transaction.objects.get(TransactionID =id)
            
            quantity = object.Quantity
            sum_quantity = former_quantity + quantity
            
            if sum_quantity > Quantity:
                new_quantity = og_quantity.QuantityInStock - Quantity
            elif sum_quantity < Quantity:
                new_quantity = og_quantity.QuantityInStock + Quantity
            else:
                new_quantity = quantity
                
            og_quantity.QuantityInStock += new_quantity
            og_quantity.save()    
            
            return redirect('purchase')
    else:        
        return render(request, 'manager/purchase_form.html', {'form':form,'purchase':purchase}) 

@login_required(login_url=settings.LOGIN_URL)
def saleView(request):
    sales = Transaction.objects.filter(TransactionType='Sale')
    formA = CustomerForm()
    formB = TransactionForm()
    products = Product.objects.all()
    
    salesq = Transaction.objects.filter()
    mySaleFilter = TransactionFilter(request.GET,queryset=salesq)
    salesItems = mySaleFilter.qs
    
    if request.method == 'POST':
        formA = CustomerForm(request.POST)
        formB = TransactionForm(request.POST)
        
        if formA.is_valid() and formB.is_valid():    
                    
            sale = formB.save(commit=False)    
            sale.TransactionType = 'Sale'  
            sale.save()     
             
            TransactionID = sale.TransactionID
            
            customer = formA.save(commit=False)
            customer.TransactionID = TransactionID
            
            
            customer.save()
            
            id = sale.ProductID
            
            quantity = sale.Quantity
            
            oq = Product.objects.get(ProductID=id)
            original_quantity = oq.QuantityInStock
            original_quantity -= quantity
            
            oq.QuantityInStock = original_quantity
            oq.save()
            
            return redirect('sale')
        
        
    else:
        context = {
            'formA':formA,
            'formB':formB, 
            'sales':sales, 
            'products':products,
            'salesItems':salesItems,
            'mySaleFilter':mySaleFilter
            }
        return render(request, 'manager/sales.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
def saleUpdateView(request,id):
    sale = Transaction.objects.get(TransactionID = id)
    form = TransactionForm(instance=sale)
    
    
    if request.method == 'POST':        
        form = TransactionForm(request.POST,instance=sale )
        
        if form.is_valid:

            former = Product.objects.get(ProductID=sale.ProductID)
            former_quantity = former.QuantityInStock 
            form.save()
            
            ProductID = form.cleaned_data['ProductID']
            Quantity = form.cleaned_data['Quantity']
            
            og_quantity = Product.objects.get(ProductID=ProductID)
            object = Transaction.objects.get(TransactionID =id)
            
            quantity = object.Quantity
            sum_quantity = former_quantity + quantity
            
            if sum_quantity > Quantity:
                new_quantity = og_quantity.QuantityInStock + Quantity
            elif sum_quantity < Quantity:
                new_quantity = og_quantity.QuantityInStock - Quantity
            else:
                new_quantity = quantity
                
            og_quantity.QuantityInStock += new_quantity
            og_quantity.save()
            return redirect('sales')
    else:        
        return render(request, 'manager/sale_Update.html', {'form':form,'former':former,'sale':sale}) 


    
@login_required(login_url=settings.LOGIN_URL)    
def suppliersView(request):
    suppliers = Supplier.objects.all()
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('suppliers')
    else: 
        return render(request, 'manager/suppliers.html', {'form':form,'suppliers':suppliers})    
    
@login_required(login_url=settings.LOGIN_URL) 
def updateSuppliers(request,id):
    supplier = Supplier.objects.get(id=id)
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST,instance=supplier)
        if form.is_valid:
            form.save()
            return redirect('suppliers')
    else: 
        return render(request, 'manager/suppliers_update.html', {'form':form,'supplier':supplier})
    
