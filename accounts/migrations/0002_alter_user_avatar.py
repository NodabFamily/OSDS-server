# Generated by Django 4.0.6 on 2022-08-18 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.URLField(default='https://osds-bucket.s3.ap-northeast-2.amazonaws.com/image/%EC%98%A4%EC%88%9C%EC%9D%B4.png'),
        ),
    ]
