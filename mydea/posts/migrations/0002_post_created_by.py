# Generated by Django 3.1.13 on 2021-09-05 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
