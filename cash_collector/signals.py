from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .models import CashCollector, Task, TaskStatus, CashCollectorStatus


@receiver(post_save, sender=Task)
def update_cash_collector_status(sender, instance, created, **kwargs):
    if not created:
        cash_collector = instance.cash_collector
        if cash_collector:
            collected_tasks = Task.objects.filter(cash_collector=cash_collector, status=TaskStatus.COLLECTED.value)
            total_collected_cash = 0.0
            task_time = None
            for task in collected_tasks:
                total_collected_cash += task.amount
                if total_collected_cash >= settings.collected_cash_threshold:
                    task_time = task.updated_at
                    break
            
            if task_time:
                if timezone.now() - task_time >= timezone.timedelta(hours=settings.frozen_status_threshold_hours):
                    cash_collector.status = CashCollectorStatus.FROZEN.value
                    cash_collector.save()
                else:
                    cash_collector.status = CashCollectorStatus.ACTIVE.value
                    cash_collector.save()
