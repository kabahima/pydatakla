from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0007_sponsorapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferenceinfo',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conferenceinfo',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]