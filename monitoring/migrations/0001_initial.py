# Generated by Django 4.0.2 on 2022-02-04 02:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('document', models.CharField(max_length=30, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
                ('region', models.CharField(max_length=30)),
                ('market_time_open', models.TimeField()),
                ('market_time_close', models.TimeField()),
                ('market_time_timezone', models.IntegerField()),
                ('market_cap', models.FloatField(null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
