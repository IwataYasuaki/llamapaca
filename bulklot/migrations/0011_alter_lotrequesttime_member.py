# Generated by Django 4.0 on 2022-01-22 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bulklot', '0010_lotrequesttime_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotrequesttime',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bulklot.member', verbose_name='メンバー'),
        ),
    ]
