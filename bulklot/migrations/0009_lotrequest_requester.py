# Generated by Django 4.0 on 2022-01-15 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bulklot', '0008_lotrequesttime_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotrequest',
            name='requester',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='申込者'),
            preserve_default=False,
        ),
    ]
