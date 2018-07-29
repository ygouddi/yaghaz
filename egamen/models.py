from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Story(models.Model):
    Lang =(
        ("AF", "Afrikanns"),
        ("SQ", "Albanian"),
        ("AR", "Arabic"),
        ("HY", "Armenian"),
        ("EU", "Basque"),
        ("BN", "Bengali"),
        ("BG", "Bulgarian"),
        ("CA", "Catalan"),
        ("KM", "Cambodian"),
        ("ZH", "Chinese(Mandarin)"),
        ("HR", "Croation"),
        ("CS", "Czech"),
        ("DA", "Danish"),
        ("NL", "Dutch"),
        ("EN", "English"),
        ("ET", "Estonian"),
        ("FJ", "Fiji"),
        ("FI", "Finnish"),
        ("FR", "French"),
        ("KA", "Georgian"),
        ("DE", "German"),
        ("EL", "Greek"),
        ("GU", "Gujarati"),
        ("HE", "Hebrew"),
        ("HI", "Hindi"),
        ("HU", "Hungarian"),
        ("IS", "Icelandic"),
        ("ID", "Indonesian"),
        ("GA", "Irish"),
        ("IT", "Italian"),
        ("JA", "Japanese"),
        ("JW", "Javanese"),
        ("KO", "Korean"),
        ("LA", "Latin"),
        ("LV", "Latvian"),
        ("LT", "Lithuanian"),
        ("MK", "Macedonian"),
        ("MS", "Malay"),
        ("ML", "Malayalam"),
        ("MT", "Maltese"),
        ("MI", "Maori"),
        ("MR", "Marathi"),
        ("MN", "Mongolian"),
        ("NE", "Nepali"),
        ("NO", "Norwegian"),
        ("FA", "Persian"),
        ("PL", "Polish"),
        ("PT", "Portuguese"),
        ("PA", "Punjabi"),
        ("QU", "Quechua"),
        ("RO", "Romanian"),
        ("RU", "Russian"),
        ("SM", "Samoan"),
        ("SR", "Serbian"),
        ("SK", "Slovak"),
        ("SL", "Slovenian"),
        ("ES", "Spanish"),
        ("SW", "Swahili"),
        ("SV", "Swedish"),
        ("TA", "Tamil"),
        ("TT", "Tatar"),
        ("TE", "Telugu"),
        ("TH", "Thai"),
        ("BO", "Tibetan"),
        ("TO", "Tonga"),
        ("TR", "Turkish"),
        ("UK", "Ukranian"),
        ("UR", "Urdu"),
        ("UZ", "Uzbek"),
        ("VI", "Vietnamese"),
        ("CY", "Welsh"),
        ("XH", "Xhosa"),
    )
    title = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField(max_length=500, null= False)
    pub_date = models.DateField(auto_now_add=True, blank=False, null=False)
    update_time = models.DateField(null=True)
    has_chapter = models.BooleanField(default=False, editable=False)
    language = models.CharField(choices=Lang, default=Lang[2], max_length=3)
    story_cover = models.FileField()

    def __str__(self):
        return self.title + " - " + self.author.username


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    chapter_number = models.IntegerField(editable=False, default=1)
    chapter_title = models.CharField(max_length=250, null=True)
    chapter = models.TextField()

    def save(self, *args, **kwargs):
        number = Chapter.objects.filter(story=self.story).count()
        story = self.story
        if not story.has_chapter:
            self.chapter_number = number + 1
            story.has_chapter = True
            story.save()
        super(Chapter, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + self.story.title


class Comments(models.Model):
    comment = models.CharField(max_length=300, blank=False, null=False)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True, blank=False, null=False)
    guest_review = models.CharField(max_length=20, blank=True, null=True)



