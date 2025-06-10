from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        location = request.POST.get('location')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on location and user type
            if user.is_superuser or location == 'System Admin':
                return redirect('/admin/')
            elif location == 'Triage':
                return redirect('/patients/search/')
            elif location == 'Counselling':
                return redirect('/treatment/plan/')
            elif location == 'Clinician':
                return redirect('/clinician/vitals/')
            elif location == 'Laboratory':
                return redirect('/laboratory/')  # Updated path for Laboratory
            elif location == 'Pharmacy':
                return redirect('/dispensary/dispense/')
            elif location == 'HMIS':
                return redirect('/hmis/')
            elif location == 'User Administration':
                return redirect('/useradmin/')
            else:
                return redirect('/')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def custom_logout(request):
    logout(request)
    return redirect('users:login')

def home(request):
    return redirect('users:login')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('users:profile')
    return render(request, 'users/profile.html')
