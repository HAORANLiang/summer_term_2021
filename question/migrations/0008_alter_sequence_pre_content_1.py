# Generated by Django 3.2.4 on 2021-08-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='pre_content_1',
            field=models.BooleanField(null=True),
        ),
    ]
