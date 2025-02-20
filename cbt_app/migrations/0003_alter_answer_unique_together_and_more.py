# Generated by Django 5.0.1 on 2024-11-16 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cbt_app", "0002_candidate_alter_answer_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="answer",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="candidate",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="candidate",
            name="exams",
            field=models.ManyToManyField(related_name="candidates", to="cbt_app.exam"),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="email",
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddConstraint(
            model_name="answer",
            constraint=models.UniqueConstraint(
                fields=("candidate", "question"),
                name="unique_answer_per_candidate_per_question",
            ),
        ),
        migrations.AddConstraint(
            model_name="option",
            constraint=models.UniqueConstraint(
                fields=("question", "text"), name="unique_option_per_question"
            ),
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="exam",
        ),
    ]
