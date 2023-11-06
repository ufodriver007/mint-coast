# Generated by Django 4.2.5 on 2023-09-29 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint_app', '0017_mmodel_description_alter_mmodel_mesh_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mesh',
            field=models.FileField(upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='mview',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo00',
            field=models.FileField(default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo01',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo02',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo03',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo04',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='photo05',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/img/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='textures',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/textures/'),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='video',
            field=models.FileField(blank=True, default=None, upload_to='./static/models/<django.db.models.fields.CharField>_<django.db.models.fields.related.ForeignKey>/'),
        ),
    ]
