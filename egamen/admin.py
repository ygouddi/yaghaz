from django.contrib import admin
from egamen.models import Story, Chapter

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'summary')
    ordering = ('pub_date',)
    search_fields = ('title', 'author')
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'writer', 'comment')
    search_fields = ('story', 'writer')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'chapter_number', 'update_time')
    search_fields = ('story', 'chapter_number')


admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
