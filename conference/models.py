from django.db import models


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to="speakers/", blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    github = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Talk(models.Model):
    TALK_TYPES = [
        ("keynote", "Keynote"),
        ("talk", "Talk"),
        ("tutorial", "Tutorial"),
        ("workshop", "Workshop"),
        ("lightning", "Lightning Talk"),
    ]

    title = models.CharField(max_length=300)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name="talks")
    talk_type = models.CharField(max_length=20, choices=TALK_TYPES, default="talk")
    description = models.TextField()
    slides_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ScheduleSlot(models.Model):
    talk = models.OneToOneField(Talk, on_delete=models.CASCADE, related_name="slot", null=True, blank=True)
    title = models.CharField(max_length=300, blank=True, help_text="Used for non-talk slots like breaks")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        label = self.talk.title if self.talk else self.title
        return f"{self.date} {self.start_time} – {label}"


class Sponsor(models.Model):
    TIERS = [
        ("platinum", "Platinum"),
        ("gold", "Gold"),
        ("silver", "Silver"),
        ("bronze", "Bronze"),
        ("community", "Community"),
    ]

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="sponsors/", blank=True, null=True)
    tier = models.CharField(max_length=20, choices=TIERS, default="bronze")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=300)
    description = models.TextField()
    url = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.sponsor.name}"


class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='hero_slides/')
    cta_label = models.CharField(max_length=80, blank=True)
    cta_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title


class Program(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=280)
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class ConferenceInfo(models.Model):
    """Singleton — only one row should exist. Controls the home hero section."""
    location_label = models.CharField(max_length=100, default="Kampala, Uganda")
    headline = models.CharField(max_length=300, default="Talks, workshops, and data sprints in Kampala")
    tagline = models.TextField(default="Join Africa's vibrant data science community for two days of inspiring talks, hands-on tutorials, and networking with fellow practitioners.")
    event_dates = models.CharField(max_length=100, default="15-16 August 2025")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=200, default="Makerere University, Kampala")
    primary_cta_label = models.CharField(max_length=80, default="Register Now")
    primary_cta_url = models.URLField(blank=True)
    secondary_cta_label = models.CharField(max_length=80, default="Explore Programs")
    secondary_cta_url = models.URLField(blank=True)
    stat_days = models.CharField(max_length=20, default="2")
    stat_talks = models.CharField(max_length=20, default="30+")
    stat_attendees = models.CharField(max_length=20, default="500+")
    stat_workshops = models.CharField(max_length=20, default="10+")

    class Meta:
        verbose_name = "Conference Info"
        verbose_name_plural = "Conference Info"

    def __str__(self):
        return "Conference Info"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CallForProposal(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='proposals')
    title = models.CharField(max_length=220)
    description = models.TextField()
    submission_url = models.URLField()
    opens_at = models.DateTimeField(blank=True, null=True)
    closes_at = models.DateTimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = ['program__title', '-is_open', 'closes_at']

    def __str__(self):
        return f"{self.program.title}: {self.title}"


class GalleryPhoto(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.caption or f"Photo {self.pk}"


class Meetup(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to='meetups/', blank=True, null=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    venue_url = models.URLField(blank=True, help_text="Google Maps or venue website link")
    registration_url = models.URLField(help_text="Link to RSVP / registration form")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.date >= timezone.localdate()


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_url = models.URLField(help_text="Link to the GitHub repository")
    demo_url = models.URLField(blank=True, help_text="Live demo or project website (optional)")
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags e.g. Python, ML, Data")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class SponsorApplication(models.Model):
    TIERS = [
        ("platinum", "Platinum"),
        ("gold", "Gold"),
        ("silver", "Silver"),
        ("bronze", "Bronze"),
        ("community", "Community"),
    ]
    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    organisation = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    website = models.URLField(blank=True)
    tier_interest = models.CharField(max_length=20, choices=TIERS, default="bronze")
    message = models.TextField(blank=True, help_text="Anything you'd like us to know")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.organisation} ({self.get_status_display()})"
