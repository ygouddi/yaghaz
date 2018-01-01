from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Story, Chapter,Comments
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, AddStroyForm, AddChapterForm
from django.utils import timezone
from django.contrib.auth.models import User


def home(request):
    stories = Story.objects.all().order_by('-pub_date')
    if request.user.is_authenticated:
        return render(request, 'index.html', {'stories': stories, 'user': request.user})
    else:
        return render(request, 'index.html', {'stories': stories})


def post(request, story_id, page=1):
    story = Story.objects.get(id=story_id)
    chapters = story.chapter_set.all()
    paginator = Paginator(chapters, 1)
    chapter = Chapter.objects.get(id=page)
    count = story.comments_set.all().count
    if request.method == 'POST':
        review = request.POST['comment']
        comment = Comments()
        comment.chapter = chapter
        comment.comment = review
        comment.story = story
        if request.user.is_authenticated:
            comment.commenter = request.user
        else:
            writer = request.POST['writer']
            print("writer is :", writer)
            if writer is None or writer == "":
                writer = "Guest"
            comment.guest_review = writer
        comment.save()
        story = chapter.story
    number = chapters.count()
    if number >= 1:
        try:
            chapters = paginator.page(page)
        except PageNotAnInteger:
            chapters = paginator.page(1)
        except EmptyPage:
            chapters = paginator.page(paginator.num_pages)
        return render(request, 'single.html', {'story': story, 'chapters': chapters, 'count' : count})


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
    fields = ('title', 'summary', 'language', 'story_cover',)
    template_name = 'edit_story.html'
    success_url = reverse_lazy('egamen:profile')

    def user_passes_test(self, request):
        if request.user.is_authenticated:
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


def userStories(request, username):
    user = User.objects.get(username=username)
    stories = Story.objects.filter(author=user).order_by('pub_date')
    return render(request,'user_page.html',{'stories' : stories})


def commentList(request, story_id, page=1):
    story = Story.objects.get(id=story_id)
    comments = story.comments_set.all()
    return render(request,'comment_list.html', {'comments': comments, 'story' : story})


def about(request):
    return render(request, 'about.html')

