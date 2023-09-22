from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.userLoginView.as_view(template_name='users/login.html'),name='login'),
    path('register/',views.userCreationView,name='register'),
    path('logout/',views.userLogoutView.as_view(),name='logout'),
    path('update_user/',views.userChangeView,name='user_update'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/reset_done.html'),name='password_reset_done'),
    path('reset/<uidb>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_complete.html'),name='password_reset_complete'),
    
    
    
    path('',views.homeView,name='home'),
    
    path('customer_update/<int:id>',views.customerUpdateView,name='customerUpdate'),
    path('customer/',views.customer_view,name='customer'),
    
    path('category_update/<int:id>',views.categoryUpdateView,name='categoryUpdate'),
    path('category/',views.categoryView,name='category'),
    
    path('product_update/<int:id>',views.productUpdateView,name='productUpdate'),
    path('product/',views.productView,name='product'),
    
    # path('purchase_create/',views.purchaseView,name='purchaseCreate'),
    path('purchase_update/<int:id>',views.purchaseUpdateView,name='purchaseUpdate'),
    path('purchases/',views.purchasesView,name='purchase'),
    
    path('sale_create/',views.saleView,name='sale'),
    path('sale_update/<int:id>',views.saleUpdateView,name='saleUpdate'),
    
    path('suppliers/',views.suppliersView,name='suppliers'),
    path('suppliers_update/<int:id>',views.updateSuppliers,name='suppliersUpdate'),
]
'''
UserCreationView
UserChangeView
PasswordResetView
homeView
customerCreationView
customerUpdateView
customer_view
categoryCreationView
categoryUpdateView
categoryView
productCreationView
productView
purchaseView
purchaseUpdateView
purchasesView
saleView
saleUpdateView
salesView
suppliersView
'''