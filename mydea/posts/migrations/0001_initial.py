# Generated by Django 3.1.13 on 2021-09-05 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified.', verbose_name='modified at')),
                ('visibility', models.CharField(blank=True, choices=[('PB', 'public'), ('PT', 'protected'), ('PV', 'private')], default='PB', max_length=2, null=True)),
                ('body', models.CharField(blank=True, max_length=280)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
