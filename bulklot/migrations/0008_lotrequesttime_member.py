# Generated by Django 4.0 on 2022-01-12 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bulklot', '0007_alter_lotrequest_location_alter_lotrequest_req_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotrequesttime',
            name='member',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.DO_NOTHING, to='bulklot.member', verbose_name='メンバー'),
            preserve_default=False,
        ),
    ]
