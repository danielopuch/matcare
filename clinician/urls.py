from django.urls import path
from . import views

app_name = 'clinician'
urlpatterns = [
    path('vitals/', views.vitals, name='vitals'),
    path('queue/', views.queue, name='queue'),
]
