import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=300)),
                ('image', models.ImageField(upload_to='hero_slides/')),
                ('cta_label', models.CharField(blank=True, max_length=80)),
                ('cta_url', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('excerpt', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('is_published', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-published_at', '-created_at']},
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('summary', models.CharField(max_length=280)),
                ('description', models.TextField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('venue', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='CallForProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('description', models.TextField()),
                ('submission_url', models.URLField()),
                ('opens_at', models.DateTimeField(blank=True, null=True)),
                ('closes_at', models.DateTimeField(blank=True, null=True)),
                ('is_open', models.BooleanField(default=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='conference.program')),
            ],
            options={'ordering': ['program__title', '-is_open', 'closes_at']},
        ),
    ]
