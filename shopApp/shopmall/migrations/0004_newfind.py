# Generated by Django 3.2.6 on 2021-10-05 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopmall', '0003_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewFind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=20)),
                ('trackid', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
    ]
