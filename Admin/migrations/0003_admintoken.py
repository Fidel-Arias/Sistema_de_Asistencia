# Generated by Django 5.0.7 on 2024-08-19 01:06

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_delete_maetipousuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminToken',
            fields=[
                ('key', models.CharField(default=uuid.uuid4, max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='Admin.maeadministrador')),
            ],
            options={
                'unique_together': {('admin_id', 'key')},
            },
        ),
    ]