from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Story(models.Model):
    Lang =(
        ('Arabic', 'AR'),
        ('Othor', 'OT')
    )
    title = models.CharField(max_length=250, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000, null= False)
    pub_date = models.DateField(auto_now_add=True, blank=False, null=False)
    has_chapter = models.BooleanField(default=False)
    lang = models.CharField(choices=Lang, default=Lang[0], max_length=3)
    story_cover = models.FileField()

    def __str__(self):
        return self.title + " - " + self.author.username





class Chapter(models.Model):
    story = models.ForeignKey(Story, related_name="story")
    title = models.CharField(max_length=100, null= False)
    chapter_number = models.IntegerField(editable=False, default=1)
    update_time = models.DateField(null=True)
    chapter = HTMLField()


    def save(self, *args, **kwargs):
        number = Chapter.objects.filter(story=self.story).count()
        self.chapter_number = number+1
        story = self.story
        if not story.has_chapter:
            story.has_chapter = True
            story.save()
        super(Chapter,self).save(*args,**kwargs)