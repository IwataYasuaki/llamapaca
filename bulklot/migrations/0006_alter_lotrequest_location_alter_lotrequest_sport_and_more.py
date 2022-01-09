# Generated by Django 4.0 on 2022-01-09 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulklot', '0005_lotrequest_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotrequest',
            name='location',
            field=models.CharField(choices=[('10,2', '舎人公園')], default='舎人公園', max_length=100),
        ),
        migrations.AlterField(
            model_name='lotrequest',
            name='sport',
            field=models.CharField(choices=[('130', 'テニス（人工芝）')], default='テニス（人工芝）', max_length=100),
        ),
        migrations.AlterField(
            model_name='lotrequesttime',
            name='time',
            field=models.CharField(choices=[('900_1100', '09:00～'), ('1100_1300', '11:00～'), ('1300_1500', '13:00～'), ('1500_1700', '15:00～'), ('1700_1900', '17:00～')], max_length=40),
        ),
    ]
