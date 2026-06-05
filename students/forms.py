from django import forms
from .models import Student
from django import forms

class StudentRegistrationForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'name',
            'email',
            'password',
            'branch',
            'semester',
            'cgpa',
            'aptitude',
            'coding',
            'communication',
            'projects'
        ]


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'branch',
            'semester',
            'cgpa',
            'aptitude',
            'coding',
            'communication',
            'projects'
        ]

class PredictionForm(forms.Form):

    cgpa = forms.FloatField()

    aptitude = forms.IntegerField()

    coding = forms.IntegerField()

    communication = forms.IntegerField()

    projects = forms.IntegerField()