from django.urls import path
from . import views

app_name = 'utils'

urlpatterns = [
    path('mock/sigaa/', views.mocked_sigaa, name='sigaa'),
    path('mock/empty/', views.mocked_empty, name='empty'),
    path('mock/table/', views.mocked_just_table, name='table')
]
