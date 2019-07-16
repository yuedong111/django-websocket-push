# Generated by Django 2.2.2 on 2019-06-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190612_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(default=1)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('check_number', models.CharField(max_length=6)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['c_time'],
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
