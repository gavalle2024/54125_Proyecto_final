# Generated by Django 4.2.11 on 2024-04-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0003_alter_entregable_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
