# Generated by Django 4.1.3 on 2022-11-06 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0005_contest_last_attempt_id_downloaded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checker.contest'),
        ),
    ]
