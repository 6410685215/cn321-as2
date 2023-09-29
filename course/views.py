from django.shortcuts import render
from users.models import Student

# Create your views here.
def index(request):
    return render(request, 'course/course.html')

def page_course(request):
    user = request.user
    admin = user.is_staff
    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,})

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