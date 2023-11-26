from django.urls import re_path
from . import views

app_name = 'utils'

urlpatterns = [
    re_path('mock/(?P<path>(sigaa|empty|table))/', views.mock_sigaa, name='sigaa'),
]
