from django.urls import path
from api.views import save_schedule, get_schedules, delete_schedule, views

app_name = 'api'

urlpatterns = [
    path('', views.Search.as_view(), name="search"),
    path('year-period/', views.YearPeriod.as_view(), name="year-period"),
    path('schedule/save/', save_schedule.SaveSchedule.as_view(), name="save-schedule"),
    path('schedule/', views.Schedule.as_view(), name="schedule"),
    path('schedules/', get_schedules.GetSchedules.as_view(), name="get-schedules"),
    path('schedules/<int:id>/', delete_schedule.DeleteSchedule.as_view(), name="delete-schedule")
]
