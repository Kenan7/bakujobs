# Generated by Django 2.1.1 on 2018-09-10 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakujobs', '0010_auto_20180910_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='user',
            new_name='owner',
        ),
    ]
