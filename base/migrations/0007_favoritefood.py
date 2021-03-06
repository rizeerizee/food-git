# Generated by Django 3.2.9 on 2022-03-06 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_customer_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.customer')),
                ('food', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.food')),
            ],
        ),
    ]
