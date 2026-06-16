from urllib import request

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
from reportlab.pdfgen import canvas
from django.contrib import messages


def home(request):

    return render(request, 'home.html')


from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

           print("FORM VALID")

           student = form.save(commit=False)

           username = student.email

           if User.objects.filter(username=username).exists():

               form.add_error(
                 'email',
                 'An account with this email already exists.'
               )

           else:

                user = User.objects.create_user(
                    username=username,
                    email=student.email,
                    password=student.password
                )

                student.user = user

                student.save()

                return redirect('/login/')

        else:

         print("FORM INVALID")
         print(form.errors)

    else:

       form = StudentRegistrationForm()

    return render(
    request,
    'register.html',
    {'form': form}
)



def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/dashboard/')
        else:

            messages.error(
                request,
                "Invalid username or password"
            )

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
    placement_probability = 0
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
        placement_probability = min(
            100,
            round(
                (
                    (student.cgpa * 10) +
                    student.aptitude +
                    student.coding +
                    student.communication +
                    (student.projects * 5)
                ) / 4
            )
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
    roadmap = []

    if student:

     if student.aptitude < 70:
        roadmap.append(
            "Practice Aptitude daily for 30 minutes"
        )

    if student.coding < 70:
        roadmap.append(
            "Solve DSA problems regularly"
        )

    if student.communication < 70:
        roadmap.append(
            "Improve communication and interview skills"
        )

    if student.projects < 3:
        roadmap.append(
            "Build more projects and upload them to GitHub"
        )

    if student.cgpa < 7:
        roadmap.append(
            "Focus on improving academic performance"
        )
    context = {

    'student': student,

    'total_predictions': total_predictions,

    'total_placed': total_placed,

    'total_not_placed': total_not_placed,

    'placement_rate': round(
        placement_rate,
        2
    ),
    'roadmap': roadmap,
    'readiness_score': readiness_score,

    'strengths': strengths,
'placement_probability': placement_probability,

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
        messages.success(
           request,
           "Profile updated successfully!"
)
        return redirect('/dashboard/')

    else:

        form = StudentProfileForm(
            instance=student
        )

    return render(
        request,
        'profile.html',
        {
            'form': form,
            'student': student
        }
    )

def predict(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    result_text = None
    guidance = None
    readiness_score = None
    placement_probability = None

    if request.method == 'POST':

        cgpa = student.cgpa
        aptitude = student.aptitude
        coding = student.coding
        communication = student.communication
        projects = student.projects

        readiness_score = round(
            (
                (cgpa * 10)
                + aptitude
                + coding
                + communication
                + (projects * 5)
            ) / 4
        )

        placement_probability = min(
            100,
            readiness_score
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
                guidance.append(
                    "Backend Developer"
                )

            if aptitude >= 80:
                guidance.append(
                    "Data Analyst"
                )

            if communication >= 80:
                guidance.append(
                    "Business Analyst"
                )

            if cgpa >= 8:
                guidance.append(
                    "Software Engineer"
                )

            if projects >= 5:
                guidance.append(
                    "Full Stack Developer"
                )

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
            'placement_probability': placement_probability,
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
    student = Student.objects.filter(
    user=request.user
    ).first()

    top_skill = None

    if student:

     scores = {

        'Aptitude': student.aptitude,

        'Coding': student.coding,

        'Communication': student.communication

    }

    top_skill = max(
        scores,
        key=scores.get
    )
    recent_predictions = PredictionHistory.objects.order_by(
        '-created_at'
    )[:5]
    placed_data = total_placed

    not_placed_data = total_not_placed
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
            'placed_data': placed_data,
            'not_placed_data': not_placed_data,
            'top_skill': top_skill,
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
def company_eligibility(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    eligible = []

    not_eligible = []

    recommended = []

    if student:

        # Eligibility Check

        if student.cgpa >= 6:
            eligible.append("TCS")
        else:
            not_eligible.append("TCS")

        if student.cgpa >= 6.5:
            eligible.append("Infosys")
        else:
            not_eligible.append("Infosys")

        if student.cgpa >= 7:
            eligible.append("Accenture")
        else:
            not_eligible.append("Accenture")

        if student.cgpa >= 7.5:
            eligible.append("Cognizant")
        else:
            not_eligible.append("Cognizant")

        if student.cgpa >= 8 and student.coding >= 80:
            eligible.append("Amazon")
        else:
            not_eligible.append("Amazon")

        if student.cgpa >= 9 and student.coding >= 90:
            eligible.append("Google")
        else:
            not_eligible.append("Google")

        if student.cgpa >= 9 and student.coding >= 90:
            eligible.append("Microsoft")
        else:
            not_eligible.append("Microsoft")

        # Recommended Companies

        if student.coding >= 90:
            recommended.append("Google")

        if student.coding >= 85:
            recommended.append("Amazon")

        if student.coding >= 75:
            recommended.append("Microsoft")

        if student.coding >= 70:
            recommended.append("Accenture")

        if student.coding >= 60:
            recommended.append("TCS")

    return render(
        request,
        'company_eligibility.html',
        {
            'student': student,
            'eligible': eligible,
            'not_eligible': not_eligible,
            'recommended': recommended
        }
    )


def download_report(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="placement_report.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setTitle("Placement Report")

    pdf.drawString(
        100,
        800,
        "PLACEMENT PREDICTION REPORT"
    )

    pdf.drawString(
        100,
        760,
        f"Name: {student.name}"
    )

    pdf.drawString(
        100,
        740,
        f"Branch: {student.branch}"
    )

    pdf.drawString(
        100,
        720,
        f"Semester: {student.semester}"
    )

    pdf.drawString(
        100,
        700,
        f"CGPA: {student.cgpa}"
    )

    pdf.drawString(
        100,
        680,
        f"Aptitude: {student.aptitude}"
    )

    pdf.drawString(
        100,
        660,
        f"Coding: {student.coding}"
    )

    pdf.drawString(
        100,
        640,
        f"Communication: {student.communication}"
    )

    pdf.drawString(
        100,
        620,
        f"Projects: {student.projects}"
    )

    readiness_score = round(
        (
            (student.cgpa * 10)
            + student.aptitude
            + student.coding
            + student.communication
            + (student.projects * 5)
        ) / 4
    )

    pdf.drawString(
        100,
        580,
        f"Readiness Score: {readiness_score}%"
    )

    strengths = []

    weaknesses = []

    if student.coding >= 80:
        strengths.append("Coding")
    else:
        weaknesses.append("Coding")

    if student.aptitude >= 70:
        strengths.append("Aptitude")
    else:
        weaknesses.append("Aptitude")

    if student.communication >= 70:
        strengths.append("Communication")
    else:
        weaknesses.append("Communication")

    if student.cgpa >= 8:
        strengths.append("Academic Performance")
    else:
        weaknesses.append("Academic Performance")

    pdf.drawString(
        100,
        540,
        "Strengths:"
    )

    y = 520

    for item in strengths:

        pdf.drawString(
            120,
            y,
            f"- {item}"
        )

        y -= 20

    pdf.drawString(
        300,
        540,
        "Areas To Improve:"
    )

    y2 = 520

    for item in weaknesses:

        pdf.drawString(
            320,
            y2,
            f"- {item}"
        )

        y2 -= 20

    pdf.save()

    return response