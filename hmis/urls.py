from django.urls import path
from . import views

app_name = 'hmis'
urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
]
