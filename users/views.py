from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Student

# Create your views here.
@csrf_exempt
def sign_in(request):
    """
    The `sign_in` function handles the logic for user authentication and login, redirecting to the admin
    page if the user is a staff member, or rendering the course page for regular users.

    :return: The function `sign_in` returns different responses depending on the request method.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request,'course/page_user.html', {'username': request.user, 
                                                            'admin': request.user.is_staff,})
        user_s = Student.objects.get(student_id=request.user)
        return render(request,'course/page_user.html', {'username': user_s.get_username(),
                                                                'admin': user.is_staff, 
                                                                'name': user_s.get_full_name(), 
                                                                'email': user_s.get_email()})
    
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is None:
                messages.error(request, "Invalid username or password")
                return render(request,'users/login.html',{'form': form, 
                                                          'messages': messages.get_messages(request)})
            
            if user.is_staff:
                login(request, user)
                return render(request,'course/page_user.html', {'username': user, 
                                                                'admin': user.is_staff,})
            else:
                user_s = Student.objects.get(student_id=user)
                login(request, user)
                return render(request,'course/page_user.html', {'username': user_s.get_username(),
                                                                'admin': user.is_staff, 
                                                                'name': user_s.get_full_name(), 
                                                                'email': user_s.get_email()})
        
        messages.error(request, "Invalid username or password")
        return render(request,'users/login.html',{'form': form})
    
def sign_out(request):
    """
    The `sign_out` function handles the logic for user logout, redirecting to the login page.

    :return: The function `sign_out` returns a redirect to the login page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')