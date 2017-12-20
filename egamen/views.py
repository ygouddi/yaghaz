from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import Story
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, AddStroyForm, AddChapterForm


def home(request):
    stories = Story.objects.all()
    if request.user.is_authenticated():
        return render(request, 'index.html', {'stories': stories, 'user':request.user})
    else:
        return render(request,'index.html',{'stories' : stories})


def chapter(request, id):
    post = Story.objects.get(id=id)
    return render(request,'single.html',{'story': post})

########FOR THE USER #################"
def register_user(request):

    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.username = username
            user.email = email
            user.save()
            return redirect('egamen:home')

    else:
        form = UserForm()
    return render(request, 'register_user.html', {'form':form})


@login_required(login_url='egamen:login')
def user_profile(request):
    user = request.user
    stories = Story.objects.filter(author=user)
    return render(request, 'user_profile.html', {'stories': stories})
########FOR THE USER #################"

def add_story(request):
    if not request.user.is_authenticated():
        return redirect('egamen:home')
    else:
        storyForm= AddStroyForm(request.POST or None, request.FILES or None)
        chapterForm = AddChapterForm(request.POST or None, request.FILES or None)
        if storyForm.is_valid() and chapterForm.is_valid():
            chapter = chapterForm.save(commit=False)
            story = storyForm.save(commit=False)
            story.author = request.user
            story.save()
            chapter.story = story
            chapter.save()
            return redirect('egamen:profile')
        context = {
            "story": storyForm,"chapter": chapterForm, 'user': request.user
        }
        return render(request, 'add_story.html', context)


@method_decorator(login_required(login_url='egamen:login'), name='dispatch')
class EditStory(UpdateView):
        model = Story
        fields = ('title', 'summary', 'lang', 'story_cover',)
        template_name = 'edit_story.html'
        success_url = reverse_lazy('egamen:profile')
