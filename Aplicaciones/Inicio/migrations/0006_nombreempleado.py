# Generated by Django 4.0.4 on 2022-04-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inicio', '0005_delete_nombreempleado'),
    ]

    operations = [
        migrations.CreateModel(
            name='NombreEmpleado',
            fields=[
                ('idnombreempleado', models.AutoField(db_column='idNombreEmpleado', primary_key=True, serialize=False)),
                ('primernombre', models.CharField(blank=True, db_column='primerNombre', max_length=50, null=True)),
                ('appaterno', models.CharField(blank=True, db_column='apPaterno', max_length=50, null=True)),
                ('apmaterno', models.CharField(blank=True, db_column='apMaterno', max_length=50, null=True)),
            ],
            options={
                'db_table': 'nombre_empleado',
                'managed': False,
            },
        ),
    ]
