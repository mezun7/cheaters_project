# Generated by Django 4.1.3 on 2022-11-10 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0010_remove_usertype_checker_usertype_name_should have or login_pcms and password or auth_type pcms_and_m'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestproblem',
            name='threshold',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
