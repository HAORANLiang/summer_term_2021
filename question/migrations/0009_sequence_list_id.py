# Generated by Django 3.2.4 on 2021-08-28 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_alter_sequence_pre_content_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='list_id',
            field=models.IntegerField(null=True),
        ),
    ]
