# Generated by Django 4.0.5 on 2022-06-15 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_productmodel_litr_delete_productlitr'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litr', models.PositiveIntegerField()),
            ],
        ),
    ]
