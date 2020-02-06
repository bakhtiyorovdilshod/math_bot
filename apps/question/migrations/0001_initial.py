# Generated by Django 3.0.2 on 2020-01-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FourChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('answer', models.TextField(max_length=100)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('numb_of_option1', models.IntegerField(blank=True, default=0, null=True)),
                ('numb_of_option2', models.IntegerField(blank=True, default=0, null=True)),
                ('numb_of_option3', models.IntegerField(blank=True, default=0, null=True)),
                ('numb_of_option4', models.IntegerField(blank=True, default=0, null=True)),
                ('message_id', models.CharField(max_length=200)),
                ('ans_false', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Second',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('answer', models.TextField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('option1', models.CharField(max_length=100)),
                ('ans_true', models.IntegerField(default=0)),
                ('ans_false', models.IntegerField(default=0)),
                ('message_id', models.CharField(max_length=200)),
            ],
        ),
    ]