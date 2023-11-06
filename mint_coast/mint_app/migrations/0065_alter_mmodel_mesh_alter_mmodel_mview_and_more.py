# Generated by Django 4.2.5 on 2023-10-30 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint_app', '0064_alter_mmodel_mesh_alter_mmodel_mview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmodel',
            name='mesh',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/', verbose_name='Файл модели'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mview',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo00',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 1'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo01',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 2'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo02',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 3'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo03',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 4'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo04',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 5'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo05',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/img/', verbose_name='Фото 6'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='textures',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/textures/', verbose_name='Архив с текстурами'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='video',
            field=models.FileField(blank=True, default=None, upload_to='./models/103023230141/', verbose_name='Файл с видео'),
        ),
    ]
