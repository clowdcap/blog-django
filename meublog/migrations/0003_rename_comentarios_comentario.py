# Generated by Django 3.2.9 on 2021-12-05 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meublog', '0002_comentarios'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comentarios',
            new_name='Comentario',
        ),
    ]
