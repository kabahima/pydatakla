from django import forms
from conference.models import (
    Speaker, Talk, ScheduleSlot, Sponsor, JobPosting,
    HeroSlide, BlogPost, Program, CallForProposal, ConferenceInfo, GalleryPhoto, Meetup, Project,
)


class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = '__all__'


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = '__all__'


class ScheduleSlotForm(forms.ModelForm):
    class Meta:
        model = ScheduleSlot
        fields = '__all__'


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = '__all__'


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = '__all__'


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = '__all__'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'


class CallForProposalForm(forms.ModelForm):
    class Meta:
        model = CallForProposal
        fields = '__all__'


class ConferenceInfoForm(forms.ModelForm):
    class Meta:
        model = ConferenceInfo
        exclude = ['id']


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = '__all__'


class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'description': forms.Textarea(attrs={'rows': 5}),
            'venue_url': forms.URLInput(attrs={'placeholder': 'https://maps.google.com/...'}),
            'registration_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['is_published'].initial = True


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'demo_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Python, ML, Data Viz'}),
        }
