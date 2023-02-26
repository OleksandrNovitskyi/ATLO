# Generated by Django 4.1.4 on 2023-02-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_rename_horisontal_collapse_results_horizontal_collapse"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="results",
            name="horizontal_collapse",
        ),
        migrations.RemoveField(
            model_name="results",
            name="vertical_collapse",
        ),
        migrations.AddField(
            model_name="results",
            name="bottom_collapse",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="results",
            name="left_collapse",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="results",
            name="right_collapse",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="results",
            name="top_collapse",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]