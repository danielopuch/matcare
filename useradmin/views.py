from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from .models import Role, UserRole

User = get_user_model()

def is_user_admin(user):
    try:
        return UserRole.objects.filter(user=user, role__name='UserAdmin').exists()
    except DatabaseError:
        # If the table doesn't exist yet, no one is an admin
        return False

@login_required
@user_passes_test(is_user_admin)
def user_admin_dashboard(request):
    users = User.objects.all()
    roles = Role.objects.all()
    user_roles = UserRole.objects.select_related('user', 'role')
    return render(request, 'useradmin/dashboard.html', {
        'users': users,
        'roles': roles,
        'user_roles': user_roles,
    })

@login_required
@user_passes_test(is_user_admin)
def assign_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        if user_id and role_id:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
            UserRole.objects.get_or_create(user=user, role=role)
    return redirect('useradmin:dashboard')
