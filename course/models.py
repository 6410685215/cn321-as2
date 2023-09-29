from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=50)
    course_doc = models.CharField(max_length=200)
    quota = models.IntegerField()
    
    def __str__(self):
        return f'{self.course_id} {self.course_name} - {self.quota}'
    
    def request_course(self):
        self.quota -= 1
        self.save()
        
    def drop_course(self):
        self.quota += 1
        self.save()