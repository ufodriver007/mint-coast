# Generated by Django 4.2.5 on 2023-11-05 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mint_app', '0087_alter_mmodel_mesh_alter_mmodel_mview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmodel',
            name='mesh',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/', verbose_name='Файл модели'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mview',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo00',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 1'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo01',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 2'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo02',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 3'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo03',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 4'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo04',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 5'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo05',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/img/', verbose_name='Фото 6'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='textures',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/textures/', verbose_name='Архив с текстурами'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='video',
            field=models.FileField(blank=True, default=None, upload_to='./models/110523153234/', verbose_name='Файл с видео'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.FileField(blank=True, default=None, upload_to='./news/110523153234/', verbose_name='Файл изображения'),
        ),
        migrations.AlterField(
            model_name='news',
            name='posted_by',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
