from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0006_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(max_length=200)),
                ('contact_name', models.CharField(max_length=200)),
                ('email', models.EmailField()),
                ('website', models.URLField(blank=True)),
                ('tier_interest', models.CharField(choices=[('platinum', 'Platinum'), ('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze'), ('community', 'Community')], default='bronze', max_length=20)),
                ('message', models.TextField(blank=True, help_text="Anything you'd like us to know")),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-submitted_at'],
            },
        ),
    ]
