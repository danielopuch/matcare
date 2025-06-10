from django.urls import path
from . import views

app_name = 'laboratory'
urlpatterns = [
    path('', views.lab_dashboard, name='dashboard'),
    path('dispense/', views.dispense, name='dispense'),
]
