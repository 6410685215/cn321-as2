from django.shortcuts import render
from users.models import Student
from .models import Course, CourseEnrollment

# Create your views here.
def index(request):
    return render(request, 'course/course.html')

def page_course(request):
    user = request.user
    admin = user.is_staff
    course = Course.objects.all()
    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': course,})

def page_user(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_user.html', { 'username': user,
                                                          'admin': admin,})
    user_s = Student.objects.get(student_id=user)
    return render(request, 'course/page_user.html', { 'username': user,
                                                      'admin': admin,
                                                      'name': user_s.get_full_name(), 
                                                      'email': user_s.get_email()})

def page_board(request):
    user = request.user
    admin = user.is_staff
    return render(request, 'course/page_board.html', { 'username': user,
                                                       'admin': admin,})
    
def course_enroll(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_course.html', { 'username': user,
                                                            'admin': admin,})
    course = Course.objects.get(course_id=request.POST['course_id'])
    course.quota -= 1
    course.save()
    course_enroll = CourseEnrollment(student_id=request.user, course_id=course)
    course_enroll.save()
    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': Course.objects.all(),})
    
def course_drop(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_course.html', { 'username': user,
                                                            'admin': admin,})
    course = Course.objects.get(course_id=request.POST['course_id'])
    course.quota += 1
    course.save()
    course_enroll = CourseEnrollment.objects.get(student_id=request.user, course_id=course)
    course_enroll.delete()
    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,})
    