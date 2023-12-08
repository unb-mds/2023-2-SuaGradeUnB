from django.urls import path
from api.views import schedules, delete_schedule, views

app_name = 'api'

urlpatterns = [
    path('', views.Search.as_view(), name="search"),
    path('year-period/', views.YearPeriod.as_view(), name="year-period"),
    path('schedules/', schedules.Schedules.as_view(), name="schedules"),
    path('schedules/<int:id>/', delete_schedule.DeleteSchedule.as_view(), name="delete-schedule"),
    path('schedules/generate/', views.GenerateSchedule.as_view(), name="generate-schedules"),
]
