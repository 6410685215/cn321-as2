from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        for m in messages.get_messages(request):
            print(m)
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print(bool(messages.get_messages(request)))
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is None:
                messages.error(request, "Invalid username or password")
                for m in messages.get_messages(request):
                    print(m)
                return render(request,'users/login.html',{'form': form, 'messages': messages.get_messages(request)})
            
            if user.is_staff:
                login(request, user)
                return redirect('admin:index')
            else:
                login(request, user)
                return render(request,'course/course.html')
        
        # form is not valid or user is not authenticated
        messages.error(request, "Invalid username or password")
        for m in messages.get_messages(request):
            print(m)
        return render(request,'users/login.html',{'form': form})