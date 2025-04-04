# Generated by Django 5.1.3 on 2025-03-20 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Transport', 'Transport'), ('Shopping', 'Shopping'), ('Bills', 'Bills'), ('Other', 'Other')], default='Other', max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
