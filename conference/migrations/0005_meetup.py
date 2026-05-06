from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_galleryphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='meetups/')),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('venue', models.CharField(max_length=200)),
                ('venue_url', models.URLField(blank=True, help_text='Google Maps or venue website link')),
                ('registration_url', models.URLField(help_text='Link to RSVP / registration form')),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date', 'time'],
            },
        ),
    ]
