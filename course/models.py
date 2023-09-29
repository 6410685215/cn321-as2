from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    quota = models.IntegerField()
    
    def __str__(self):
        return f'{self.course_id} {self.course_name} - {self.quota}'
    
class CourseEnrollment(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student_id} {self.course_id.course_id}'