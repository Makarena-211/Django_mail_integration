from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.index, name='index')
]