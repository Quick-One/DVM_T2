# Generated by Django 4.1.5 on 2023-01-15 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('option_A', models.CharField(max_length=100)),
                ('option_B', models.CharField(max_length=100)),
                ('option_C', models.CharField(max_length=100)),
                ('option_D', models.CharField(max_length=100)),
                ('answer', models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1)),
                ('questionaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questionaire')),
            ],
        ),
    ]