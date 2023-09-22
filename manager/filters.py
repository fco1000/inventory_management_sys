import  django_filters 
from .models import Customer,Transaction

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['IDNo']
        
class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['TransactionID']