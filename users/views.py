from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def sign_in(request):
    """
    The `sign_in` function handles the logic for user authentication and login, redirecting to the admin
    page if the user is a staff member, or rendering the course page for regular users.

    :return: The function `sign_in` returns different responses depending on the request method.
    """
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
                return render(request,'users/login.html',{'form': form, 'messages': messages.get_messages(request)})
            
            if user.is_staff:
                login(request, user)
                return redirect('admin:index', {'user': user.get_username()})
            else:
                login(request, user)
                return render(request,'course/course.html', {'user': user.get_username()})
        
        messages.error(request, "Invalid username or password")
        return render(request,'users/login.html',{'form': form})