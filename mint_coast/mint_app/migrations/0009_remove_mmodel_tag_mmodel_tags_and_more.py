# Generated by Django 4.2.5 on 2023-09-29 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint_app', '0008_alter_mmodel_created_with'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mmodel',
            name='tag',
        ),
        migrations.AddField(
            model_name='mmodel',
            name='tags',
            field=models.CharField(choices=[('Art', 'Art'), ('Prop', 'Prop'), ('Stylized', 'Stylized'), ('Automotive', 'Automotive'), ('3D Art', '3D Art')], default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='created_with',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='mmodel',
            name='style',
            field=models.CharField(choices=[('Stylized', 'Stylized'), ('Realistic', 'Realistic'), ('Anime', 'Anime'), ('Cartoon', 'Cartoon')], default=None, max_length=300),
        ),
    ]
