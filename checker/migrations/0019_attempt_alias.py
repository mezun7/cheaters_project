# Generated by Django 4.1.3 on 2022-11-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0018_alter_attemptscheckjobs_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='alias',
            field=models.IntegerField(null=True),
        ),
    ]
