from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from .utils import BaseChoicesEnum


class CashCollectorStatus(BaseChoicesEnum):
    ACTIVE = "active"
    FROZEN = "frozen"


class TaskStatus(BaseChoicesEnum):
    PENDING = "pending" # default: when a task is created
    STARTING = "STARTING" # when a cash collector starts a task
    COLLECTED = "collected" # when a cash collector completes a task
    DELIVERED = "delivered" # when a cash collector delivers the collected cash to the manager
    CANCELLED = "cancelled" # when a task is cancelled by the manager


class AbstractModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractContactInfo(AbstractModel):
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    class Meta:
        abstract = True


class Manager(AbstractContactInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "managers"
        ordering = ["user__username"]

    @property
    def full_name(self):
        return self.user.get_full_name()
    
    @property
    def email(self):
        return self.user.email
    

class CashCollector(AbstractContactInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE, related_name="cash_collectors")
    status = models.CharField(max_length=20, choices=CashCollectorStatus.choices(), default=CashCollectorStatus.ACTIVE.value)
    
    class Meta:
        db_table = "cash_collectors"
        ordering = ["user__username"]
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    @property
    def email(self):
        return self.user.email
    

class Customer(AbstractContactInfo):
    name = models.CharField(max_length=256)
    email = models.EmailField()

    class Meta:
        db_table = "customers"
        

class Task(AbstractModel):
    manager = models.ForeignKey("Manager", on_delete=models.CASCADE, related_name="tasks")
    cash_collector = models.ForeignKey("CashCollector", on_delete=models.CASCADE, related_name="tasks")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(max_length=20, choices=TaskStatus.choices(), default=TaskStatus.PENDING.value)
    amount_due = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    amount_due_at = models.DateTimeField()

    class Meta:
        db_table = "tasks"
        ordering = ["-created_at"]
