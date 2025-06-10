from django.urls import path
from . import views

app_name = 'patients'
urlpatterns = [
    path('register/', views.patient_register, name='register_patient'),
    path('search/', views.patient_search, name='search_patient'),
    path('dashboard/<int:patient_id>/', views.patient_dashboard, name='dashboard'),
]
