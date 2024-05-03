# Generated by Django 4.2.11 on 2024-05-03 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ort_test', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resultanswer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.question'),
        ),
        migrations.AddField(
            model_name='resultanswer',
            name='result_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.results'),
        ),
        migrations.AddField(
            model_name='resultanalysis',
            name='result_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.results'),
        ),
        migrations.AddField(
            model_name='resultanalysis',
            name='topic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.topics'),
        ),
        migrations.AddField(
            model_name='resultanalysis',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='topic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.topics'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ort_test.question'),
        ),
    ]
