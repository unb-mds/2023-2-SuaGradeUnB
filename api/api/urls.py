from django.urls import path
from api.views import save_schedule, views

app_name = 'api'

urlpatterns = [
    path('', views.Search.as_view(), name="search"),
    path('year-period/', views.YearPeriod.as_view(), name="year-period"),
    path('schedule/save/', save_schedule.SaveSchedule.as_view(), name="save-schedule"),
    path('schedule/', views.Schedule.as_view(), name="schedule")
]
