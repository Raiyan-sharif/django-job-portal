from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(role):
    """Allow one user type only, and make sure the profile exists."""

    def decorator(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.user_type != role:
                messages.error(request, 'That page is not available for your account type.')
                return redirect('dashboard')
            if not request.user.has_profile():
                messages.info(request, 'Create your profile first.')
                return redirect('profile')
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


recruiter_required = role_required('recruiter')
jobseeker_required = role_required('jobseeker')