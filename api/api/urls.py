from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('', views.Search.as_view(), name="search")
]