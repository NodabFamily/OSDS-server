# Generated by Django 4.0.6 on 2022-07-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
