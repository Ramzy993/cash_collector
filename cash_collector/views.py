from rest_framework import viewsets
from rest_framework.response import Response

from .models import Customer, Manager, CashCollector, Task, TaskStatus, CashCollectorStatus
from .serializers import CustomerSerializer, ManagerSerializer, CashCollectorSerializer, TaskSerializer



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def start_cash_collector_task(self, request, *args, **kwargs):
        try:
            cash_collector = CashCollector.objects.get(pk=request.user.cash_collector.pk)
            task = Task.objects.get(cash_collector=cash_collector, pk=kwargs["pk"])
            task.status = TaskStatus.STARTING.value
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except CashCollector.DoesNotExist:
            return Response({"detail": "Cash collector not found."}, status=404)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=404)    
    
    def collect_cash_collector_task(self, request, *args, **kwargs):
        try: 
            cash_collector = CashCollector.objects.get(pk=request.user.cash_collector.pk)
            task = Task.objects.get(cash_collector=cash_collector, pk=kwargs["pk"])
            task.status = TaskStatus.COLLECTED.value
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except CashCollector.DoesNotExist:
            return Response({"detail": "Cash collector not found."}, status=404)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=404)
    
    def deliver_cash_collector_task(self, request, *args, **kwargs):
        try:
            manager = Manager.objects.get(pk=request.user.manager.pk)
            task = Task.objects.get(manager=manager, pk=kwargs["pk"])
            task.status = TaskStatus.DELIVERED.value
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Manager.DoesNotExist:
            return Response({"detail": "Manager not found."}, status=404)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=404)


class CashCollectorViewSet(viewsets.ModelViewSet):
    queryset = CashCollector.objects.all()
    serializer_class = CashCollectorSerializer
    
    def get_cash_collector_status(self, request, *args, **kwargs):
        try:
            cash_collector = CashCollector.objects.get(pk=request.user.cash_collector.pk)
            serializer = CashCollectorSerializer(cash_collector)
            return Response({"status": serializer.data["status"]})
        except CashCollector.DoesNotExist:
            return Response({"detail": "Cash collector not found."}, status=404)
        
    def get_cash_collector_tasks(self, request, *args, **kwargs):
        try:
            cash_collector = CashCollector.objects.get(pk=request.user.cash_collector.pk)
            queryset = Task.objects.filter(cash_collector=cash_collector).order_by("created_at")
            serializer = TaskSerializer(queryset, many=True)
            return Response(serializer.data)
        except CashCollector.DoesNotExist:
            return Response({"detail": "Cash collector not found."}, status=404)
    
    def get_cash_collector_next_pending_tasks(self, request, *args, **kwargs):
        try:
            cash_collector = CashCollector.objects.get(pk=request.user.cash_collector.pk)
            if cash_collector.status == CashCollectorStatus.FROZEN.value:
                return Response({"detail": "Cash collector is frozen."}, status=400)
            queryset = Task.objects.filter(cash_collector=cash_collector, status=TaskStatus.PENDING.value).order_by("created_at")
            serializer = TaskSerializer(queryset)
            return Response(serializer.data)
        except CashCollector.DoesNotExist:
            return Response