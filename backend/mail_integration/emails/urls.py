from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('login/', views.login_view, name='login_view')
]