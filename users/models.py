from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    student_id = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    def __str__(self):
        return self.student_id.username
