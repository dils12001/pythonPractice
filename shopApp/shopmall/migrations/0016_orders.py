# Generated by Django 3.2.6 on 2021-10-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopmall', '0015_carts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(max_length=20)),
                ('userId', models.CharField(max_length=20)),
                ('progress', models.IntegerField()),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
    ]