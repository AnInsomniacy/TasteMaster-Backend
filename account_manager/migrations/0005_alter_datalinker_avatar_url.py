# Generated by Django 4.2 on 2024-03-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0004_alter_datalinker_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datalinker',
            name='avatar_url',
            field=models.CharField(default='https://qiniu.jingpin365.com/uploads/weibo/201912/9e16d1d636af8434d50e1241bb59163e.jpeg', max_length=10000),
        ),
    ]
