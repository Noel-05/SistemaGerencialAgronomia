# Generated by Django 3.2 on 2021-04-29 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_alter_docente_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiouniversitario',
            name='codigo_carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.carrera'),
        ),
    ]
