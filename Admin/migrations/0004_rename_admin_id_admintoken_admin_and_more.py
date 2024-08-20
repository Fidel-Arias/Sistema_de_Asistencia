# Generated by Django 5.0.7 on 2024-08-19 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_admintoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admintoken',
            old_name='admin_id',
            new_name='admin',
        ),
        migrations.AlterUniqueTogether(
            name='admintoken',
            unique_together={('admin', 'key')},
        ),
    ]