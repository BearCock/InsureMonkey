# Generated by Django 4.1.6 on 2023-03-01 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insuremonkey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nastavitpojisteni',
            name='pojistenec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insuremonkey.pojistenec', verbose_name='Pojištěnec'),
        ),
    ]
