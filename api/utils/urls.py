from django.urls import path
from .views import mocked_departments

app_name = 'utils'

urlpatterns = [
    path('mock/departments/', mocked_departments, name='departments'),
]
