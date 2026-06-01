from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, StudentProfileForm
from .models import Student

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
def profile(request):

    if request.method == 'POST':

        form = StudentProfileForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/dashboard/')

    else:

        form = StudentProfileForm()

    return render(request, 'profile.html', {'form': form})
def predict(request):

    students = Student.objects.all()

    if not students:
        return render(
            request,
            'prediction.html',
            {
                'message': 'No student profile found.'
            }
        )

    student = students.last()

    score = (
        (student.cgpa * 10)
        + (student.aptitude * 0.25)
        + (student.coding * 0.30)
        + (student.communication * 0.20)
        + (student.projects * 5)
    )

    if score >= 150:
        category = "High Chance"

        roles = [
            "Backend Developer",
            "Python Developer",
            "Data Analyst"
        ]

    elif score >= 120:
        category = "Moderate Chance"

        roles = [
            "Software Developer",
            "QA Engineer",
            "Support Engineer"
        ]

    else:
        category = "Low Chance"

        roles = [
            "Skill Development Required",
            "Practice DSA",
            "Build More Projects"
        ]

    context = {
        'score': round(score, 2),
        'category': category,
        'roles': roles
    }

    return render(request, 'prediction.html', context)