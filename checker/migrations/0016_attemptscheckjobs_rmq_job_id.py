# Generated by Django 4.1.3 on 2022-11-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0015_alter_attemptscheckjobs_script_checking_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptscheckjobs',
            name='rmq_job_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
