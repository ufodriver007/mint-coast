# Generated by Django 4.2.5 on 2023-10-03 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint_app', '0018_delete_tag_alter_mmodel_mesh_alter_mmodel_mview_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mmodel',
            name='is_textures',
        ),
        migrations.RemoveField(
            model_name='mmodel',
            name='is_video',
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='format',
            field=models.CharField(choices=[('obj', 'obj'), ('fbx', 'fbx'), ('max', 'max'), ('mo', 'mo'), ('stl', 'stl')], default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mesh',
            field=models.FileField(upload_to='./static/models/100323090514/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mview',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo00',
            field=models.FileField(default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo01',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo02',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo03',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo04',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo05',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='textures',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/textures/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='video',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323090514/'),
        ),
    ]
