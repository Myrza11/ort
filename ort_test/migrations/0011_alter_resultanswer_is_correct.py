# Generated by Django 4.2.11 on 2024-04-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ort_test', '0010_alter_results_scheduled_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultanswer',
            name='is_correct',
            field=models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='UNCOMPLETED', max_length=10),
        ),
    ]
