# Generated by Django 3.2.5 on 2021-08-04 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_string', models.CharField(max_length=20)),
                ('session', models.CharField(choices=[('W', 'Winter'), ('S', 'Summer')], max_length=1)),
                ('year', models.CharField(max_length=4)),
                ('dept', models.CharField(max_length=4)),
                ('course', models.CharField(max_length=4)),
                ('section', models.CharField(max_length=3)),
                ('only_general', models.BooleanField()),
                ('sms', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=30)),
            ],
            options={
                'unique_together': {('course_string', 'email')},
            },
        ),
    ]
