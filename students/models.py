from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    branch = models.CharField(max_length=50, blank=True)

    semester = models.IntegerField(default=0)

    cgpa = models.FloatField(default=0)

    aptitude = models.IntegerField(default=0)

    coding = models.IntegerField(default=0)

    communication = models.IntegerField(default=0)

    projects = models.IntegerField(default=0)

    def __str__(self):
        return self.name
class PredictionHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    cgpa = models.FloatField()

    aptitude = models.IntegerField()

    coding = models.IntegerField()

    communication = models.IntegerField()

    projects = models.IntegerField()

    prediction = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.student.name} - {self.prediction}"