from django.urls import path
from . import views

app_name = 'useradmin'
urlpatterns = [
    path('', views.user_admin_dashboard, name='dashboard'),
    path('assign-role/', views.assign_role, name='assign_role'),
]
