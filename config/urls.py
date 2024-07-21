"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cash_collector.views import TaskViewSet, CashCollectorViewSet

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")), 
    path('admin/', admin.site.urls),
    path(
        "cash-collector/tasks/",
        CashCollectorViewSet.as_view({"get": "get_cash_collector_tasks"}),
        name="cash-collector-tasks",
    ),
    path(
        "cash-collector/tasks/next_task/",
        CashCollectorViewSet.as_view({"get": "get_cash_collector_next_pending_tasks"}),
        name="cash-collector-tasks-next-pending",
    ),
    path(
        "cash-collector/status/",
        CashCollectorViewSet.as_view({"get": "get_cash_collector_status"}),
        name="cash-collector-status",
    ),
    path(
        "tasks/<int:pk>/start/",
        TaskViewSet.as_view({"patch": "start_cash_collector_task"}),
        name="cash-collector-tasks-start",
    ),
    path(
        "tasks/<int:pk>/collect/",
        TaskViewSet.as_view({"patch": "collect_cash_collector_task"}),
        name="cash-collector-tasks-collect",
    ),
    path(
        "tasks/<int:pk>/pay/",
        TaskViewSet.as_view({"patch": "deliver_cash_collector_task"}),
        name="manager-tasks-deliver",
    ),
    
]
