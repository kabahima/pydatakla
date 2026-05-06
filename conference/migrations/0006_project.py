from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0005_meetup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('github_url', models.URLField(help_text='Link to the GitHub repository')),
                ('demo_url', models.URLField(blank=True, help_text='Live demo or project website (optional)')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags e.g. Python, ML, Data', max_length=200)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-is_featured', '-created_at'],
            },
        ),
    ]
