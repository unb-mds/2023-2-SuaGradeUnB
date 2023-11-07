from django.urls import path
from .views import mocked_departments
import sys

app_name = 'utils'

urlpatterns = []

if 'test' in sys.argv:
    urlpatterns += [
        path('departments/', mocked_departments, name='departments'),
    ]
