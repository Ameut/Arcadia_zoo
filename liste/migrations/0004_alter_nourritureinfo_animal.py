# Generated by Django 5.0.6 on 2024-05-14 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liste', '0003_remove_nourritureinfo_rapport_nourritureinfo_animal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nourritureinfo',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nourritures', to='liste.animal'),
        ),
    ]
