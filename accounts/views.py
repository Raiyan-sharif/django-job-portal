from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegistrationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.display_name}! Your account is ready.')
        return redirect('home')

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
    return render(request, 'accounts/home.html')