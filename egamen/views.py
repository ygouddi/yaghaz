from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from .models import Story, Chapter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, AddStroyForm, AddChapterForm
from django.utils import timezone


def home(request):
    stories = Story.objects.all()
    if request.user.is_authenticated:
        return render(request, 'index.html', {'stories': stories, 'user': request.user})
    else:
        return render(request, 'index.html', {'stories': stories})


def post(request, id_story):
    story = Story.objects.get(id=id_story)
    posts = story.chapter_set.all()
    paginator = Paginator(posts, 1)
    page = request.GET.get('page',1)
    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)
    return render(request, 'single.html', {'story': story, 'chapters': chapters})


########FOR THE USER #################"
def register_user(request):
    if request.method == 'POST':
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
    return render(request, 'register_user.html', {'form': form})


@login_required(login_url='egamen:login')
def user_profile(request):
    user = request.user
    stories = Story.objects.filter(author=user)
    return render(request, 'user_profile.html', {'stories': stories})


########FOR THE USER #################"

@login_required
def add_story(request):
    storyForm = AddStroyForm(request.POST or None, request.FILES or None)
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
        "story": storyForm, "chapter": chapterForm, 'user': request.user
    }
    return render(request, 'add_story.html', context)


"""Delete Story"""
def delete_story(request, id):
    story = Story.objects.get(id=id)
    story.delete()
    return redirect('egamen:profile')


@method_decorator(login_required(login_url='egamen:login'), name='dispatch')
class EditStory(UpdateView):
    model = Story
    fields = ('title', 'summary', 'lang', 'story_cover',)
    template_name = 'edit_story.html'
    success_url = reverse_lazy('egamen:profile')

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.author == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('stories:login_user')
        return super(EditStory, self).dispatch(
            request, *args, **kwargs)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.update_time = timezone.now()
        post.save()
        return redirect('egamen:profile')


@login_required
def manageChapter(request, id):
    form = AddChapterForm(request.POST or None)
    if form.is_valid():
        chapter = form.save(commit=False)
        story = Story.objects.get(id=id)
        chapter.story = story
        chapter.save()
        return redirect('egamen:profile')
    context = {'chapter': form, 'user': request.user}
    return render(request, 'manage_chapters.html', context)
