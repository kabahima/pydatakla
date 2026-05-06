from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0002_heroslide_blogpost_program_callforproposal'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_label', models.CharField(default='Kampala, Uganda', max_length=100)),
                ('headline', models.CharField(default='Talks, workshops, and data sprints in Kampala', max_length=300)),
                ('tagline', models.TextField(default="Join Africa's vibrant data science community for two days of inspiring talks, hands-on tutorials, and networking with fellow practitioners.")),
                ('event_dates', models.CharField(default='15-16 August 2025', max_length=100)),
                ('venue', models.CharField(default='Makerere University, Kampala', max_length=200)),
                ('primary_cta_label', models.CharField(default='Register Now', max_length=80)),
                ('primary_cta_url', models.URLField(blank=True)),
                ('secondary_cta_label', models.CharField(default='Explore Programs', max_length=80)),
                ('secondary_cta_url', models.URLField(blank=True)),
                ('stat_days', models.CharField(default='2', max_length=20)),
                ('stat_talks', models.CharField(default='30+', max_length=20)),
                ('stat_attendees', models.CharField(default='500+', max_length=20)),
                ('stat_workshops', models.CharField(default='10+', max_length=20)),
            ],
            options={
                'verbose_name': 'Conference Info',
                'verbose_name_plural': 'Conference Info',
            },
        ),
    ]
