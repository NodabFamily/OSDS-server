# Generated by Django 4.0.6 on 2022-08-19 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0002_alter_family_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='password',
            field=models.CharField(default='', max_length=127, null=True),
        ),
    ]
