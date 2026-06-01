from django.db import models

from django.db import models

class Student(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    branch = models.CharField(max_length=50, blank=True)

    semester = models.IntegerField(default=1)

    cgpa = models.FloatField(default=0)

    aptitude = models.IntegerField(default=0)

    coding = models.IntegerField(default=0)

    communication = models.IntegerField(default=0)

    projects = models.IntegerField(default=0)

    def __str__(self):
        return self.name
