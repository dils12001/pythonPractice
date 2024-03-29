# Generated by Django 3.2.6 on 2021-10-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopmall', '0012_auto_20211014_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userAccount', models.CharField(max_length=20, unique=True)),
                ('userPasswd', models.CharField(max_length=20)),
                ('userNickName', models.CharField(max_length=20)),
                ('userPhone', models.CharField(max_length=20)),
                ('userAddress', models.CharField(max_length=100)),
                ('userImg', models.CharField(max_length=150)),
                ('userRank', models.IntegerField()),
                ('userToken', models.CharField(max_length=50)),
            ],
        ),
    ]
