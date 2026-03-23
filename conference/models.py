from django.db import models


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='speakers/', blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    github = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Talk(models.Model):
    TALK_TYPES = [
        ('keynote', 'Keynote'),
        ('talk', 'Talk'),
        ('tutorial', 'Tutorial'),
        ('workshop', 'Workshop'),
        ('lightning', 'Lightning Talk'),
    ]

    title = models.CharField(max_length=300)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name='talks')
    talk_type = models.CharField(max_length=20, choices=TALK_TYPES, default='talk')
    description = models.TextField()
    slides_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ScheduleSlot(models.Model):
    talk = models.OneToOneField(Talk, on_delete=models.CASCADE, related_name='slot', null=True, blank=True)
    title = models.CharField(max_length=300, blank=True, help_text='Used for non-talk slots like breaks')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        label = self.talk.title if self.talk else self.title
        return f"{self.date} {self.start_time} – {label}"


class Sponsor(models.Model):
    TIERS = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('community', 'Community'),
    ]

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    tier = models.CharField(max_length=20, choices=TIERS, default='bronze')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=300)
    description = models.TextField()
    url = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.sponsor.name}"
