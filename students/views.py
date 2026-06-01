from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm


def home(request):

    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/')

    else:

        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/dashboard/')

    return render(request, 'login.html')
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    return render(request, 'dashboard.html')
def logout_view(request):

    logout(request)

    return redirect('/')
