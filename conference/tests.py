from django.test import TestCase
from django.urls import reverse

from .models import Speaker, Talk, ScheduleSlot, Sponsor, JobPosting
import datetime


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('conference:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PyData')

    def test_home_shows_featured_talks(self):
        speaker = Speaker.objects.create(name='Alice', bio='Data scientist')
        Talk.objects.create(
            title='Intro to Pandas',
            speaker=speaker,
            talk_type='talk',
            description='A deep dive into pandas.',
            is_featured=True,
        )
        response = self.client.get(reverse('conference:home'))
        self.assertContains(response, 'Intro to Pandas')


class TalksViewTests(TestCase):
    def test_talks_page_loads(self):
        response = self.client.get(reverse('conference:talks'))
        self.assertEqual(response.status_code, 200)

    def test_talks_list_shows_talks(self):
        speaker = Speaker.objects.create(name='Bob', bio='ML engineer')
        Talk.objects.create(
            title='Machine Learning in Production',
            speaker=speaker,
            talk_type='tutorial',
            description='How to deploy ML models.',
        )
        response = self.client.get(reverse('conference:talks'))
        self.assertContains(response, 'Machine Learning in Production')


class TalkDetailViewTests(TestCase):
    def test_talk_detail_page_loads(self):
        speaker = Speaker.objects.create(name='Carol', bio='Data engineer')
        talk = Talk.objects.create(
            title='Data Pipelines',
            speaker=speaker,
            talk_type='talk',
            description='Building robust pipelines.',
        )
        response = self.client.get(reverse('conference:talk_detail', args=[talk.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Data Pipelines')

    def test_talk_detail_404_for_missing_talk(self):
        response = self.client.get(reverse('conference:talk_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class SpeakersViewTests(TestCase):
    def test_speakers_page_loads(self):
        response = self.client.get(reverse('conference:speakers'))
        self.assertEqual(response.status_code, 200)

    def test_speakers_page_lists_speakers(self):
        Speaker.objects.create(name='Dave', bio='Statistician')
        response = self.client.get(reverse('conference:speakers'))
        self.assertContains(response, 'Dave')


class ScheduleViewTests(TestCase):
    def test_schedule_page_loads(self):
        response = self.client.get(reverse('conference:schedule'))
        self.assertEqual(response.status_code, 200)

    def test_schedule_shows_slots(self):
        speaker = Speaker.objects.create(name='Eve', bio='Researcher')
        talk = Talk.objects.create(
            title='NLP in Luganda',
            speaker=speaker,
            talk_type='talk',
            description='Natural language processing for local languages.',
        )
        ScheduleSlot.objects.create(
            talk=talk,
            date=datetime.date(2025, 8, 15),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(10, 45),
            room='Hall A',
        )
        response = self.client.get(reverse('conference:schedule'))
        self.assertContains(response, 'NLP in Luganda')


class SponsorsViewTests(TestCase):
    def test_sponsors_page_loads(self):
        response = self.client.get(reverse('conference:sponsors'))
        self.assertEqual(response.status_code, 200)

    def test_sponsors_page_shows_sponsors(self):
        Sponsor.objects.create(name='DataCorp', tier='gold', website='https://datacorp.example.com')
        response = self.client.get(reverse('conference:sponsors'))
        self.assertContains(response, 'DataCorp')


class ConductViewTests(TestCase):
    def test_conduct_page_loads(self):
        response = self.client.get(reverse('conference:conduct'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Code of Conduct')


class AboutViewTests(TestCase):
    def test_about_page_loads(self):
        response = self.client.get(reverse('conference:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PyData Kampala')


class ModelStrTests(TestCase):
    def test_speaker_str(self):
        s = Speaker(name='Frank')
        self.assertEqual(str(s), 'Frank')

    def test_talk_str(self):
        speaker = Speaker.objects.create(name='Grace', bio='AI researcher')
        talk = Talk(title='AI Ethics', speaker=speaker)
        self.assertEqual(str(talk), 'AI Ethics')

    def test_sponsor_str(self):
        sp = Sponsor(name='TechFund')
        self.assertEqual(str(sp), 'TechFund')
