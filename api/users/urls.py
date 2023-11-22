from django.urls import re_path, path
from users import views

app_name = 'users'

urlpatterns = [
    re_path('register/' + r'(?P<oauth2>[^/]+)/$', views.Register.as_view(), name='register'),
    path('login/', views.RefreshJWTView.as_view(), name='login'),
    path('logout/', views.BlacklistJWTView.as_view(), name='logout'),
]
