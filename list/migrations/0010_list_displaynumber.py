# Generated by Django 3.2.6 on 2021-08-29 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0009_list_show_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='displayNumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
