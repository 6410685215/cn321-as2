from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    ID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    quota = models.IntegerField()
    
    def __str__(self):
        return f'{self.ID} {self.name} - {self.quota}'
    
class Enroll(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student_id} {self.course_id.ID}'