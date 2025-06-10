from django.urls import path
from . import views

app_name = 'dispensary'
urlpatterns = [
    path('dispense/', views.dispense, name='dispense'),
]
