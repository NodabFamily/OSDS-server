
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('archives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='photo',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_image',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_image',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archives.photo')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(fields=('user_id', 'photo_id'), name='unique_user_photo_bookmark'),
        ),
    ]
