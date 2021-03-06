# Generated by Django 4.0 on 2022-05-14 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bulklot', '0013_alter_lotrequesttime_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.CharField(max_length=100, verbose_name='希望日時')),
                ('sport', models.CharField(max_length=100, verbose_name='種目')),
                ('location', models.CharField(max_length=100, verbose_name='公園名')),
                ('result', models.CharField(max_length=40, verbose_name='抽選結果')),
                ('pubdate', models.DateField(verbose_name='取得日')),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bulklot.member', verbose_name='メンバー')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='所有者')),
            ],
        ),
    ]
