from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import (JobSeekerProfileForm, LoginForm, RecruiterProfileForm,
                    RegistrationForm)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.display_name}! Now create your profile.')
        return redirect('profile')

    return render(request, 'accounts/register.html', {'form': form})


class PortalLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You have signed out.')
    return redirect('login')


@login_required
def home_view(request):
    return redirect('dashboard')


@login_required
def profile_view(request):
    """Creates the profile the first time, and edits it after that."""
    user = request.user
    if user.is_recruiter:
        form_class = RecruiterProfileForm
        instance = getattr(user, 'recruiter_profile', None)
    else:
        form_class = JobSeekerProfileForm
        instance = getattr(user, 'jobseeker_profile', None)

    is_new = instance is None
    form = form_class(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.instance.user = user
        form.save()
        messages.success(request, 'Profile created.' if is_new else 'Profile saved.')
        return redirect('dashboard')

    return render(request, 'accounts/profile.html', {'form': form, 'is_new': is_new})