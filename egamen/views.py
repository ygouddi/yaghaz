from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Story
from .forms import UserForm, UserLogin





def home(request):
    stories = Story.objects.all()
    if request.user.is_authenticated():
        return render(request, 'index.html', {'stories': stories, 'user':request.user})
    else:
        return render(request,'index.html',{'stories' : stories})



def chapter(request, story_id):
    post = Story.objects.get(id=story_id)
    return render(request,'single.html',{'story': post})


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('egamen:home')
            else:
                return render(request, 'login_user.html', {'error_message': "your account has been disabled"})
        else:
            return render(request, 'login_user.html', {'error_message': 'Wrong Username or Password'})
    elif request.user.is_authenticated():
        return redirect('stories:home')
    else:
        return render(request, 'login_user.html')

def register_user(request):

    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.username  = username
            user.email = email
            user.save()
            return redirect('egamen:home')
    else:
        form = UserForm()
        return render(request, 'register_user.html', {'form':form})


def logout_user(request):
    logout(request)
    return redirect('egamen:home')