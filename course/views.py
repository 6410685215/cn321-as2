from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'course/course.html')

def page_course(request):
    return render(request, 'course/page_course.html')

def page_user(request):
    return render(request, 'course/page_user.html')

def page_board(request):
    return render(request, 'course/page_board.html')