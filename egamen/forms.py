from django import forms
from .models import Story, Chapter, Comments
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='username', widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email    = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password']




class AddStroyForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label="Title",
                            widget=forms.TextInput(attrs={'placeholder': 'Story Title'}))
    summary = forms.CharField(max_length=500, label="Summary",
                             widget=forms.Textarea(attrs={'placeholder': 'Summary', 'rows': 4}))
    story_cover = forms.FileField(required=False)

    class Meta:
        model = Story
        fields = ['title', 'summary', 'language', 'story_cover']


class AddChapterForm(forms.ModelForm):
    chapter = forms.CharField(widget=SummernoteWidget())
    title = forms.CharField(max_length=250, label='chapter title',
                            widget=forms.TextInput(attrs={'placeholder': 'give it a title'}))

    class Meta:
        model = Chapter
        fields = ['chapter', 'title']


class CommentForm(forms.ModelForm):
    commenter = forms.CharField(max_length=20, label="commenter",
                            widget=forms.TextInput(attrs={'placeholder': ''}))
    summary = forms.CharField(max_length=300, label="comment",
                              widget=forms.Textarea(attrs={'placeholder': 'Summary', 'rows': 4}))

    class Meta:
        model = Comments
        fields = ['comment']
