# Generated by Django 4.1.5 on 2023-01-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_question_rename_responder_response_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='penalty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='reward',
            field=models.PositiveIntegerField(default=0),
        ),
    ]