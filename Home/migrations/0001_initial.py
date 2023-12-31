# Generated by Django 4.2.7 on 2023-11-03 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=10)),
                ('age', models.CharField(max_length=3)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('bloodgroup', models.CharField(max_length=10)),
                ('casepaper', models.CharField(max_length=10)),
                ('otp', models.CharField(max_length=6)),
                ('verify', models.CharField(default=0, max_length=1)),
                ('image', models.ImageField(default='default.jpg', upload_to='med_report')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('did', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=10)),
                ('age', models.CharField(max_length=3)),
                ('gender', models.CharField(max_length=10)),
                ('Department', models.CharField(max_length=20)),
                ('attendance', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=15)),
                ('salary', models.CharField(max_length=10)),
                ('otp', models.CharField(max_length=6)),
                ('verify', models.CharField(default=0, max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
