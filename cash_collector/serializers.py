from rest_framework import serializers

from .models import Customer, Manager, CashCollector, Task


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = "__all__"
        
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"
        

class CashCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashCollector
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"