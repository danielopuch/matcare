from django import template
from django.db import DatabaseError

register = template.Library()

@register.filter
def has_useradmin(user):
    try:
        from useradmin.models import UserRole
        return UserRole.objects.filter(user=user, role__name='UserAdmin').exists()
    except (ImportError, DatabaseError):
        # Return False if the model or table doesn't exist yet
        return False
