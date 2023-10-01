from django.shortcuts import render
from users.models import Student
from .models import Course, Enroll

# Create your views here.
def index(request):
    return render(request, 'course/course.html')

def page_course(request):
    user = request.user
    admin = user.is_staff
    course = Course.objects.all()
    enroll = Enroll.objects.filter(student_id=user)
    enroll = enroll.values_list('course_id', flat=True)    

    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': course,
                                                        'enroll': enroll,})

def page_user(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_user.html', { 'username': user,
                                                          'admin': admin,})
    user_s = Student.objects.get(ID=user)
    return render(request, 'course/page_user.html', { 'username': user,
                                                      'admin': admin,
                                                      'name': user_s.get_full_name(), 
                                                      'email': user_s.email,})

def page_board(request):
    user = request.user
    admin = user.is_staff
    return render(request, 'course/page_board.html', { 'username': user,
                                                       'admin': admin,})
    
def course_enroll(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return page_course(request)
    
    course = Course.objects.get(ID=request.POST['course_id'])
    course.quota -= 1
    if course.quota < 0:
        return page_course(request)
    course.save()
    course_enroll = Enroll(student_id=user, course_id=course)
    course_enroll.save()
    return page_course(request)
    
def course_drop(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_course.html', { 'username': user,
                                                            'admin': admin,})
    course = Course.objects.get(ID=request.POST['course_id'])
    course.quota += 1
    course.save()
    course_enroll = Enroll.objects.get(student_id=user, course_id=course)
    course_enroll.delete()
    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,})
    