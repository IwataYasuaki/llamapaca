# Generated by Django 4.0 on 2022-05-14 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulklot', '0012_lotrequesttime_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotrequesttime',
            name='result',
            field=models.CharField(choices=[('10', '未取得'), ('15', '取得中'), ('20', '取得失敗'), ('30', '当選'), ('40', '当選(確定済)'), ('50', '落選')], default='10', max_length=40, verbose_name='抽選結果'),
        ),
    ]
