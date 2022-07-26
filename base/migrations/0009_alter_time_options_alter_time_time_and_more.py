# Generated by Django 4.0.6 on 2022-08-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_time_timezone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='time',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='time',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='timezone',
            field=models.CharField(default='PST', max_length=20),
        ),
    ]
