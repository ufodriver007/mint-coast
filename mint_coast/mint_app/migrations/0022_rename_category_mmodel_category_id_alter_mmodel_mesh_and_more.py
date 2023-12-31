# Generated by Django 4.2.5 on 2023-10-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint_app', '0021_alter_mmodel_created_with_alter_mmodel_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mmodel',
            old_name='category',
            new_name='category_id',
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mesh',
            field=models.FileField(upload_to='./static/models/100323101003/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mview',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo00',
            field=models.FileField(upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo01',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo02',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo03',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo04',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo05',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='textures',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/textures/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='video',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/100323101003/'),
        ),
    ]
