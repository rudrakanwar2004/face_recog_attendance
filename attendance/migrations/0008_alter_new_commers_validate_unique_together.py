# Generated by Django 5.1 on 2024-09-04 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0007_alter_new_commers_validate_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="new_commers_validate",
            unique_together={("f_name", "l_name")},
        ),
    ]
