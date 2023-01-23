# Generated by Django 4.1.5 on 2023-01-23 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('reward', models.IntegerField(default=0)),
                ('penalty', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='response',
            old_name='responder',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='response',
            name='answer',
        ),
        migrations.AlterField(
            model_name='questionaire',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.question')),
                ('option_A', models.CharField(max_length=100)),
                ('option_B', models.CharField(max_length=100)),
                ('option_C', models.CharField(max_length=100)),
                ('option_D', models.CharField(max_length=100)),
                ('answer', models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1)),
            ],
            bases=('quiz.question',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceResponse',
            fields=[
                ('response_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.response')),
                ('answer', models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1)),
            ],
            bases=('quiz.response',),
        ),
        migrations.CreateModel(
            name='NumQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.question')),
                ('answer', models.IntegerField()),
            ],
            bases=('quiz.question',),
        ),
        migrations.CreateModel(
            name='NumResponse',
            fields=[
                ('response_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.response')),
                ('answer', models.IntegerField()),
            ],
            bases=('quiz.response',),
        ),
        migrations.CreateModel(
            name='TFQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.question')),
                ('answer', models.BooleanField()),
            ],
            bases=('quiz.question',),
        ),
        migrations.CreateModel(
            name='TFResponse',
            fields=[
                ('response_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.response')),
                ('answer', models.BooleanField()),
            ],
            bases=('quiz.response',),
        ),
        migrations.AddField(
            model_name='question',
            name='questionaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questionaire'),
        ),
        migrations.AlterField(
            model_name='response',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
        ),
        migrations.DeleteModel(
            name='MCQuestion',
        ),
    ]