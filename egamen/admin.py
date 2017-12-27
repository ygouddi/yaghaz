from django.contrib import admin
from egamen.models import Story, Chapter
from django_summernote.admin import SummernoteModelAdmin

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'summary')
    ordering = ('pub_date',)
    search_fields = ('title', 'author')
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'writer', 'comment')
    search_fields = ('story', 'writer')

class ChapterAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title','story', 'chapter_number')
    search_fields = ('story', 'chapter_number')
    summer_note_fields = ('chapter',)


admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
