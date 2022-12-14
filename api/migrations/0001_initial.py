# Generated by Django 4.1.3 on 2022-11-05 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('reason', models.CharField(max_length=250)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='givers', to='api.users')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='takers', to='api.users')),
            ],
        ),
    ]
