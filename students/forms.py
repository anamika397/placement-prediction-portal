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
widgets = { 
    'name': forms.TextInput(attrs={ 
        'class': 'form-control', 
        'placeholder': 'Enter full name' }),
          'email': forms.EmailInput(attrs={ 
              'class': 'form-control', 
              'placeholder': 'Enter email' }), 
              'password': forms.PasswordInput(attrs={ 
                  'class': 'form-control',
                    'placeholder': 'Create password' }),
                      'branch': forms.TextInput(attrs={
                           'class': 'form-control',
                             'placeholder': 'Branch' }), 
                             'semester': forms.NumberInput(attrs={ 
                                 'class': 'form-control' }), 
                                 'cgpa': forms.NumberInput(attrs={ 
                                     'class': 'form-control' }), 
                                     'aptitude': forms.NumberInput(attrs={
                                          'class': 'form-control' }),
                                            'coding': forms.NumberInput(attrs={ 
                                                'class': 'form-control' }),
                                                  'communication': forms.NumberInput(attrs={ 
                                                      'class': 'form-control' }), 
                                                      'projects': forms.NumberInput(attrs={
                                                           'class': 'form-control' }), 
                                                           }

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

        widgets = {

            'branch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter branch'
            }),

            'semester': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter semester'
            }),

            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CGPA'
            }),

            'aptitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Aptitude score'
            }),

            'coding': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Coding score'
            }),

            'communication': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Communication score'
            }),

            'projects': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of projects'
            }),
        }

class PredictionForm(forms.Form):

    cgpa = forms.FloatField()

    aptitude = forms.IntegerField()

    coding = forms.IntegerField()

    communication = forms.IntegerField()

    projects = forms.IntegerField()