from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, StudentProfileForm
from .models import Student
from ml.predict import predict_placement
from .forms import PredictionForm
from .ml_utils import predict_placement
from .models import PredictionHistory
import csv
from django.http import HttpResponse




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

    student = Student.objects.filter(
        user=request.user
    ).first()

    total_predictions = PredictionHistory.objects.count()

    total_placed = PredictionHistory.objects.filter(
        prediction="Placed"
    ).count()

    total_not_placed = PredictionHistory.objects.filter(
        prediction="Not Placed"
    ).count()

    if total_predictions > 0:

        placement_rate = (
            total_placed / total_predictions
        ) * 100

    else:

        placement_rate = 0

    readiness_score = 0
    strengths = []
    weaknesses = []
    if student:

        readiness_score = round(
            (
                (student.cgpa * 10) +
                student.aptitude +
                student.coding +
                student.communication +
                (student.projects * 5)
            ) / 4
        )
    if student.coding >= 80:
     strengths.append("Coding")
    else:
     weaknesses.append("Coding")


    if student.aptitude >= 80:
     strengths.append("Aptitude")
    else:
     weaknesses.append("Aptitude")


    if student.communication >= 80:
     strengths.append("Communication")
    else:
     weaknesses.append("Communication")


    if student.cgpa >= 8:
     strengths.append("Academic Performance")
    else:
     weaknesses.append("Academic Performance")


    if student.projects >= 5:
     strengths.append("Projects")
    else:
     weaknesses.append("Projects")
    context = {

    'student': student,

    'total_predictions': total_predictions,

    'total_placed': total_placed,

    'total_not_placed': total_not_placed,

    'placement_rate': round(
        placement_rate,
        2
    ),

    'readiness_score': readiness_score,

    'strengths': strengths,

    'weaknesses': weaknesses
}
    return render(
        request,
        'dashboard.html',
        context
    )

def logout_view(request):

    logout(request)

    return redirect('/')
def profile(request):

    student = Student.objects.filter(
        user=request.user
    ).first()
    print("Current student:", student)
    if request.method == 'POST':

        form = StudentProfileForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            return redirect('/dashboard/')

    else:

        form = StudentProfileForm(
            instance=student
        )

    return render(
        request,
        'profile.html',
        {
            'form': form
        }
    )

def predict(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    result_text = None
    guidance = None
    readiness_score = None

    if request.method == 'POST':

        cgpa = student.cgpa
        aptitude = student.aptitude
        coding = student.coding
        communication = student.communication
        projects = student.projects

        readiness_score = round(
            (
                (cgpa * 10) +
                aptitude +
                coding +
                communication +
                (projects * 5)
            ) / 4
        )

        result = predict_placement(
            cgpa,
            aptitude,
            coding,
            communication,
            projects
        )

        if result == 1:

            result_text = "Placed"

            guidance = []

            if coding >= 80:
                guidance.append("Backend Developer")

            if aptitude >= 80:
                guidance.append("Data Analyst")

            if communication >= 80:
                guidance.append("Business Analyst")

            if cgpa >= 8:
                guidance.append("Software Engineer")

            if projects >= 5:
                guidance.append("Full Stack Developer")

            if not guidance:
                guidance.append(
                    "Junior Software Developer"
                )

        else:

            result_text = "Not Placed"

            guidance = [
                "Improve Coding Skills",
                "Build More Projects",
                "Practice Aptitude",
                "Improve Communication"
            ]

        request.session['guidance'] = guidance
        request.session['prediction'] = result_text

        PredictionHistory.objects.create(
            student=student,
            cgpa=cgpa,
            aptitude=aptitude,
            coding=coding,
            communication=communication,
            projects=projects,
            prediction=result_text
        )

    history = PredictionHistory.objects.filter(
    student=student
).order_by(
    '-created_at'
)

    return render(
        request,
        'predict.html',
        {
            'student': student,
            'result': result_text,
            'history': history,
            'guidance': guidance,
            'readiness_score': readiness_score,
        }
    )
def history(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    history = PredictionHistory.objects.filter(
        student=student
    ).order_by('-created_at')

    return render(
        request,
        'history.html',
        {
            'history': history
        }
    )
def delete_history(request, id):

    prediction = PredictionHistory.objects.get(id=id)

    prediction.delete()

    return redirect('/history/')
def analytics(request):

    total_predictions = PredictionHistory.objects.count()

    total_placed = PredictionHistory.objects.filter(
        prediction="Placed"
    ).count()

    total_not_placed = PredictionHistory.objects.filter(
        prediction="Not Placed"
    ).count()

    recent_predictions = PredictionHistory.objects.order_by(
        '-created_at'
    )[:5]

    if total_predictions > 0:
        placement_rate = (
            total_placed / total_predictions
        ) * 100
    else:
        placement_rate = 0

    return render(
        request,
        'analytics.html',
        {
            'total_predictions': total_predictions,
            'total_placed': total_placed,
            'total_not_placed': total_not_placed,
            'placement_rate': round(placement_rate, 2),
            'recent_predictions': recent_predictions
        }
    )
def career_guidance(request):

    guidance = request.session.get(
        'guidance',
        []
    )

    prediction = request.session.get(
        'prediction',
        ''
    )

    return render(
        request,
        'career_guidance.html',
        {
            'guidance': guidance,
            'prediction': prediction
        }
    )
def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="prediction_history.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Student',
        'CGPA',
        'Aptitude',
        'Coding',
        'Communication',
        'Projects',
        'Prediction',
        'Date'
    ])

    predictions = PredictionHistory.objects.all()

    for item in predictions:

        writer.writerow([
            item.student.name,
            item.cgpa,
            item.aptitude,
            item.coding,
            item.communication,
            item.projects,
            item.prediction,
            item.created_at
        ])

    return response