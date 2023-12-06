from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('', views.Search.as_view(), name="search"),
    path('year-period/', views.YearPeriod.as_view(), name="year-period"),
    path('schedule/save/',views.SaveSchedule.as_view(), name="save-schedule")
]
